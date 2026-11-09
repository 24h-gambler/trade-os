# Implementation Plan

**Goal** Ship a concierge MVP in 4 weeks and a production MVP in 12 weeks for the first corridor (China → Korea) and first vertical (1688 K-beauty/accessories sellers). The codebase is corridor-config driven: new corridors are config + partners, not a rewrite.

---

## 1. Repository layout

```
waybill/
  apps/
    web/            # seller PWA (Next.js)
    supplier/       # supplier portal (Next.js)
    ops/            # internal ops/compliance console (Next.js)
    api/            # backend (NestJS)
  packages/
    domain/         # entities, state machines, business rules
    ledger/         # double-entry ledger library
    ui/             # shared design system
    config/         # env, feature flags, corridor config
  infra/
    terraform/      # AWS: VPC, EKS, RDS, S3, KMS
    docker/         # local dev, images
  docs/
  .github/workflows/
```

**Rules**
- Domain logic lives in `packages/domain`; API handlers are thin.
- Ledger postings are append-only; no updates/deletes.
- Every partner call goes through an adapter with idempotency and circuit breaker.
- Corridor-specific rules (currency, partners, tax) are config, not code.

---

## 2. Tech stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind, PWA | fast iteration, mobile-first |
| Backend | NestJS (TypeScript) | shared types, modular |
| Database | PostgreSQL 16 + Prisma | relational integrity, migrations |
| Cache/queue | Redis + SQS | sessions, rate limits, async jobs |
| Workflow | Temporal | saga, retries, compensation |
| Events | Kafka or SQS/SNS | domain events, integrations |
| Storage | S3 (WORM for documents) | document retention |
| Auth | WebAuthn/passkey + OIDC | FaceID/TouchID, no passwords |
| KYC | Persona/Sumsub | KYB/KYC, sanctions |
| OCR | Google Document AI/AWS Textract + LLM | invoice/PI extraction |
| Observability | OpenTelemetry, Grafana, Sentry | traces, metrics, errors |
| Infra | AWS Seoul + Singapore, EKS, Terraform | latency, data residency |

---

## 3. Data model (core tables)

```sql
create table sellers (
  id uuid primary key,
  business_no text unique not null,
  name text not null,
  tax_type text not null,          -- general | simplified | exempt
  kyc_tier int not null default 0,
  status text not null default 'active',
  created_at timestamptz not null default now()
);

create table suppliers (
  id uuid primary key,
  country text not null,
  name text not null,
  currency text not null,
  bank_account jsonb,
  export_right boolean not null default false,
  kyc_tier int not null default 0,
  status text not null default 'active',
  created_at timestamptz not null default now()
);

create table quotes (
  id uuid primary key,
  seller_id uuid references sellers(id),
  supplier_id uuid references suppliers(id),
  currency text not null,
  goods_amount numeric(18,2) not null,
  fx_rate numeric(18,6) not null,
  breakdown jsonb not null,
  total_krw numeric(18,2) not null,
  hs_code text,
  hs_confidence numeric(4,3),
  expires_at timestamptz not null,
  created_at timestamptz not null default now()
);

create table payments (
  id uuid primary key,
  quote_id uuid references quotes(id),
  seller_id uuid references sellers(id),
  supplier_id uuid references suppliers(id),
  status text not null,
  amount_usd numeric(18,2) not null,
  amount_krw numeric(18,2) not null,
  trade_model text not null,       -- agency | principal
  idempotency_key text unique not null,
  created_at timestamptz not null default now(),
  funded_at timestamptz,
  settled_at timestamptz
);

create table payment_events (
  id uuid primary key,
  payment_id uuid references payments(id),
  from_status text,
  to_status text not null,
  actor text not null,
  reason text,
  created_at timestamptz not null default now()
);

create table payouts (
  id uuid primary key,
  payment_id uuid references payments(id),
  partner text not null,
  currency text not null,
  amount numeric(18,2) not null,
  status text not null,
  tx_hash text,
  created_at timestamptz not null default now()
);

create table documents (
  id uuid primary key,
  type text not null,              -- pi | invoice | bl | declaration | tax_invoice
  hash text not null,
  version int not null,
  s3_key text not null,
  ocr_json jsonb,
  confidence numeric(4,3),
  created_at timestamptz not null default now()
);

create table customs_declarations (
  id uuid primary key,
  payment_id uuid references payments(id),
  declaration_no text,
  duty numeric(18,2),
  vat numeric(18,2),
  status text not null,
  filed_at timestamptz,
  cleared_at timestamptz
);

create table credit_lines (
  id uuid primary key,
  seller_id uuid references sellers(id),
  limit_krw numeric(18,2) not null,
  used_krw numeric(18,2) not null default 0,
  apr numeric(6,4) not null,
  status text not null
);

create table ledger_accounts (
  id uuid primary key,
  code text unique not null,
  type text not null,              -- asset | liability | revenue | expense | equity
  currency text not null
);

create table journal_entries (
  id uuid primary key,
  payment_id uuid,
  source_type text not null,
  source_id text not null,
  created_at timestamptz not null default now()
);

create table postings (
  id uuid primary key,
  journal_entry_id uuid references journal_entries(id),
  account_id uuid references ledger_accounts(id),
  debit numeric(18,2) not null default 0,
  credit numeric(18,2) not null default 0,
  currency text not null,
  constraint balanced check (debit >= 0 and credit >= 0)
);
```

**Invariants**
- Sum of debits = sum of credits per journal entry (enforced in `packages/ledger`).
- Client funds and operating funds use different account ranges.
- No posting without a `source_type` and `source_id`.
- Every payment has at least one document hash before `PAYOUT_QUEUED`.

---

## 4. API contract

### 4.1 Create quote

```http
POST /v1/quotes
Idempotency-Key: 7f0c...
Content-Type: application/json
```

```json
{
  "seller_id": "sel_123",
  "supplier_id": "sup_456",
  "invoice": {
    "currency": "USD",
    "amount": 10000,
    "incoterm": "FOB",
    "description": "cosmetic packaging, PET, 50ml",
    "hs_code": "3923.30",
    "origin": "CN"
  },
  "destination": "KR",
  "payment_terms": "NET_30"
}
```

```json
{
  "quote_id": "qte_789",
  "expires_at": "2026-11-09T13:10:00+09:00",
  "fx_rate": 1350.0,
  "breakdown": {
    "goods_krw": 13500000,
    "freight_insurance_krw": 675000,
    "duty_krw": 1134000,
    "vat_krw": 1530900,
    "platform_fee_krw": 243000,
    "credit_cost_krw": 202500
  },
  "total_krw": 17285400,
  "hs_confidence": 0.93
}
```

### 4.2 Create payment

```http
POST /v1/payments
Idempotency-Key: 9a1b...
```

```json
{ "quote_id": "qte_789", "payment_method": "VIRTUAL_ACCOUNT" }
```

```json
{
  "payment_id": "pay_001",
  "status": "AWAITING_FUNDS",
  "virtual_account": { "bank": "KB", "number": "123-456-789", "expires_at": "..." }
}
```

### 4.3 Webhooks

```json
{
  "event": "payout.settled",
  "payment_id": "pay_001",
  "partner": "hk_mso_a",
  "currency": "CNY",
  "amount": 72000,
  "tx_hash": "0x...",
  "occurred_at": "2026-11-09T13:05:00+09:00"
}
```

**Rules:** HMAC signature, 3 retries with exponential backoff, idempotent consumers, event log.

---

## 5. Payment state machine

```
QUOTED
  → AWAITING_FUNDS
  → FUNDS_RECEIVED
  → COMPLIANCE_REVIEW
  → PAYOUT_QUEUED
  → PAYOUT_INITIATED
  → PAYOUT_SETTLED
  → DOCS_IN_PROGRESS
  → CUSTOMS_FILED
  → CUSTOMS_CLEARED
  → CLOSED
```

**Exceptions:** `EXPIRED`, `CANCELLED`, `ON_HOLD`, `REJECTED`, `PAYOUT_FAILED`, `DISPUTED`, `REFUNDED`.

**Rules**
- No transition without an event row.
- `COMPLIANCE_REVIEW` requires KYB + sanctions + invoice match.
- `PAYOUT_QUEUED` requires a document hash.
- `PAYOUT_FAILED` retries with a different partner; if all fail, refund.

---

## 6. Partner adapters

| Adapter | Interface | Sandbox |
|---|---|---|
| Bank/PG | `collect()`, `refund()`, `status()` | bank sandbox |
| HK MSO | `quoteFx()`, `payoutCny()`, `status()` | partner UAT |
| Customs broker | `classify()`, `file()`, `status()` | broker sandbox |
| KYC | `verifyBusiness()`, `screenSanctions()` | Persona/Sumsub sandbox |
| Credit funder | `apply()`, `draw()`, `repay()` | funder UAT |

**Pattern:** adapter + circuit breaker + idempotency key + raw payload log. No partner call inside a DB transaction.

---

## 7. Six two-week sprints

### Sprint 0 (weeks 1–2): foundation

- Monorepo, CI, staging, auth, seller KYB, DB schema.
- **Acceptance:** a seller can sign up, upload a business license, and see an empty dashboard.

### Sprint 1 (weeks 3–4): quote

- PI upload, OCR extraction, quote engine, FX lock, landed-cost UI.
- **Acceptance:** 20 real PIs produce a quote with a breakdown; p95 <300ms; quote snapshot immutable.

### Sprint 2 (weeks 5–6): payment

- Checkout, PG virtual account, payment saga, status page, webhooks.
- **Acceptance:** a sandbox payment moves `QUOTED → FUNDS_RECEIVED → PAYOUT_QUEUED`; idempotent retries.

### Sprint 3 (weeks 7–8): supplier + ledger

- Supplier onboarding, payout adapter, double-entry ledger, reconciliation job.
- **Acceptance:** a $10k payment produces balanced journal entries; 3-way reconciliation passes on sandbox data.

### Sprint 4 (weeks 9–10): documents + customs

- Document engine, 3-way match, customs broker adapter, tax invoice generation.
- **Acceptance:** a payment cannot reach `PAYOUT_SETTLED` without a matched invoice/BL; declaration draft generated.

### Sprint 5 (weeks 11–12): pilot hardening

- Ops console, case queue, metrics, credit application, load test.
- **Acceptance:** 10 sellers, 30 payments, $500k GMV, zero losses; reconciliation 99%; on-call runbook.

---

## 8. Test plan

| Test | What | Pass |
|---|---|---|
| Unit | quote math, ledger balance, state transitions | 90%+ coverage on domain/ledger |
| Integration | partner sandbox, webhooks, idempotency | all adapters green |
| E2E | seller journey: PI → quote → pay → docs → close | 10/10 runs |
| Reconciliation | partner vs bank vs ledger | 99% matched by 10:00 KST |
| Compliance | KYB, sanctions, invoice mismatch | 100% blocked |
| Load | 100 payments/min | p95 <800ms |
| Security | auth, RBAC, secrets, pen test | no critical/high |

---

## 9. Deployment

- **Environments:** dev, staging, prod.
- **CI:** lint, typecheck, unit, integration, build, migrate.
- **CD:** EKS, blue/green, automated rollback.
- **Secrets:** AWS Secrets Manager + KMS.
- **Data:** Postgres multi-AZ; S3 WORM for documents; daily backups.
- **Observability:** traces (quote → payment → payout → customs), business dashboards, alerts for payout failures/reconciliation breaks.

---

## 10. Build vs buy

| Capability | Build | Buy/partner | Why |
|---|---|---|---|
| Quote/landed cost | ● | | differentiation |
| Payment saga | ● | | core |
| Ledger | ● | | core |
| KYC/OCR | | ● | speed |
| Sanctions | | ● | data |
| FX/on-off ramp | | ● | licenses |
| Payout | | ● | coverage |
| Customs | | ● | broker |
| Credit underwriting | ● | | data |
| Custody | | ● | security |
| Insurance | | ● | capital |

---

## 11. First six weeks checklist

- [ ] Choose the cluster (e.g., Guangzhou cosmetics packaging).
- [ ] Sign 5 suppliers for the pilot.
- [ ] Get 5 sellers to share their last five payments.
- [ ] Build the quote engine with real PIs.
- [ ] Get bank/PG sandbox access.
- [ ] Get HK MSO quote and UAT access.
- [ ] Get customs broker API/portal access.
- [ ] Legal opinion scoped (FX, trade agency, VASP partner).
- [ ] 3 paid pilots signed.
- [ ] Reconciliation spreadsheet + ledger design reviewed.

---

**KR 요약** — 12주 안에 1개 corridor(중국→한국), 1개 vertical(1688 K-beauty)용 MVP를 만든다. 6개 스프린트: 기반 → 견적 → 결제 → 공급사/원장 → 문서/통관 → 파일럿. 핵심은 랜딩 코스트, 문서 매칭, 복식부기 원장, 파트너 어댑터다.
