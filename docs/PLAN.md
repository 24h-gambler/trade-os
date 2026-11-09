# Trade OS — Execution Plan

**Goal** Prove the wedge in 90 days: 10 sellers, 30 payments, $500k GMV, zero losses, three repeat sellers. Then raise a seed and productize.

---

## 1. 90-day plan (week by week)

| Week | Focus | Deliverable | Pass criteria |
|---|---|---|---|
| 1 | Customer discovery | 30 seller interviews, 10 supplier interviews | 10 sellers share last 5 payments |
| 2 | Cost stack | 5 quotes from banks/agencies, landed-cost model | median all-in 3%+ / 5 days+ |
| 3 | Legal structure | scope opinion: trade agency/IoR, FX, VASP partner | structure viable |
| 4 | Partner letters | bank/PG, HK MSO, customs broker term sheets | 2 partners ready for sandbox |
| 5 | Concierge setup | spreadsheet ledger, manual payment flow, supplier onboarding | first 3 sellers signed |
| 6 | First payments | 5 payments, manual quote, manual payout | 0 errors, 0 losses |
| 7 | Supplier cluster | 10 suppliers onboarded, receivables account | 5 active |
| 8 | Volume | 10 sellers, 15 payments | $200k GMV |
| 9 | Documents | customs broker integration, tax invoice template | 10 declarations filed |
| 10 | Reconciliation | 3-way reconciliation, ledger review | 99% matched |
| 11 | Credit pilot | 3 sellers, 30-day terms, funding partner | 0 default |
| 12 | Case study | 1 case study, 3 repeat sellers | go/no-go |
| 13 | Fundraise or extend | seed deck, metrics, legal pack | 3 investor meetings |

**Kill criteria:** median all-in <2%; 4% payers are mostly tax evaders; suppliers refuse third-party payout; compliance cost >1%; CAC payback >9 months.

---

## 2. Twelve-month roadmap

| Quarter | Product | Commercial | Metrics |
|---|---|---|---|
| Q1 | concierge, quote, manual payments | 10 sellers, 10 suppliers | $500k GMV, 0 losses |
| Q2 | checkout, OCR, supplier portal, ledger | 50 sellers, 30 suppliers | $3M/month |
| Q3 | credit, escrow, second corridor (Vietnam) | 100 sellers, credit pilot | $6M/month, 0.2% loss |
| Q4 | partner API, multi-corridor, principal model | 200 sellers, 2 corridors | $10M/month |

---

## 3. Team and hiring

| Role | When | Why |
|---|---|---|
| CEO (trade/finance) | now | customer, partners, fundraise |
| CTO (payments/ledger) | now | architecture, build |
| COO (customs/logistics) | month 2 | broker, suppliers, ops |
| Head of Supplier Network | month 2 | cluster onboarding |
| Compliance/AML | month 3 | KYB, sanctions, TBML |
| Engineers | 1 → 3 → 6 | quote, payment, document, ledger |
| Credit risk | month 9 | underwriting, collections |

---

## 4. Budget (first 12 months)

| Item | Amount |
|---|---:|
| Salaries (4–6 people) | $400k–600k |
| Legal/regulatory | $40k–80k |
| Partner integrations | $30k–50k |
| Cloud/infra | $20k–40k |
| Sales/community | $30k–50k |
| Contingency | $50k |
| **Total** | **$570k–870k** |

Seed: $3–5M for 18 months, including credit facility readiness.

---

## 5. Partners

| Partner | Role | Status |
|---|---|---|
| Bank/PG | client funds, FX, outbound | LOI / sandbox |
| HK MSO/VASP | USDC → CNH | UAT |
| Customs broker | HS, declaration, duty/VAT | API/portal |
| KYC vendor | KYB, sanctions | sandbox |
| Credit funder | 30/60-day capital | term sheet |
| Insurance | cargo/credit | quote |

**Rule:** no single partner >50% of volume; every adapter has a fiat fallback.

---

## 6. Pilot design and metrics

| Metric | Target |
|---|---:|
| Sellers | 10 |
| Payments | 30 |
| GMV | $500k |
| Take rate | 2.5–3.0% |
| Gross margin after partner cost | 1.2%+ |
| Loss rate | 0 |
| Repeat (60 days) | 3 sellers |
| Time-to-pay | <1 day after documents |
| Reconciliation | 99% by 10:00 KST |

**Weekly dashboard:** GMV, payments, take rate, partner cost, time-to-pay, document error rate, seller NPS, supplier NPS.

---

## 7. Risks and mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Korean FX/trade law | medium | high | trade agency/IoR; bank partner; legal opinion |
| China FX/crypto rules | high | high | HK MSO, export declaration, no direct USDC to factory |
| AML/TBML | medium | high | KYB, invoice matching, sanctions, case management |
| Credit loss | medium | high | small limits, insurance, funding partner, first loss |
| Partner dependency | high | medium | multi-partner, fiat fallback |
| Incumbent response | high | medium | supplier graph, data, credit, speed |
| Small ICP | medium | high | 20 receipts + 30 interviews before scaling |
| Regulatory change | medium | medium | legal monitoring, corridor config |

---

## 8. Fundraising

**Ask:** $500k–1M pre-seed (or YC $500k) for 12–18 months.

**Use of funds**
- 2 engineers, 1 ops/compliance, 1 supplier network.
- Legal: FX, trade, customs, tax, VASP partner.
- Partner integrations and pilot.

**Milestones for seed**
- 50 sellers, $3M/month GMV, 1 corridor.
- 1.2%+ gross margin after partner cost.
- 0.3% loss rate, 40% repeat.
- Credit pilot with a funding partner.

---

## 9. Operating cadence

- **Daily:** payment exceptions, partner status, reconciliation breaks.
- **Weekly:** GMV, take rate, loss, seller/supplier NPS, pipeline.
- **Monthly:** cohort retention, unit economics, compliance review, partner review.
- **Quarterly:** corridor expansion gate, credit risk review, fundraise update.

---

**KR 요약** — 90일 안에 10 셀러·30 결제·$500k GMV·손실 0을 만들고, 12개월 안에 50 셀러·월 $3M GMV·신용 파일럿까지 간다. 팀은 CEO/CTO/COO + 컴플라이언스 + 엔지니어 3명, 예산은 $570k~870k.
