# Product

**One-liner** An SME importer uploads a factory invoice, sees the landed cost, pays in one tap, and gets customs/tax documents plus 30-day credit. The factory receives local currency. We start with Korea → China.

---

## 1. Customer

### 1.1 ICP

| Dimension | Definition |
|---|---|
| Firmographics | First market: Korean LLC, $1–10M annual GMV, imports $500k–5M/year from China/Vietnam, 5–50 employees. Expansion: any SME importer with the same profile. |
| Buying behavior | Buys from 1688 or a factory directly; uses a payment agency or trade agency; 10–30 payments/month |
| Buyer | Owner or CFO. No procurement team; the owner handles payments and customs |
| Trigger | B2B buyer demands a tax invoice; Amazon/Coupang expansion; bank loan requires documents; agency failure; volume outgrows manual processing |
| Anti-ICP | Hobby sellers; sellers whose margin depends on tax evasion; large importers with bank relationships and cheap credit |

**Expansion:** any SME importer in Vietnam, Mexico, Indonesia, or Turkey — same architecture, new corridor config and local partners.

### 1.2 Why now for the customer

- 1688 blocks Korean cards. Sellers must use an agency or a Chinese account.
- Payment agencies charge 2–5%; full-service agencies 6–11%.
- The seller cannot see the all-in landed cost until after customs.
- Coupang/Amazon payouts arrive 30–60 days after the sale.
- The seller has no credit history that a bank will underwrite.

---

## 2. Problem

The seller buys a **bundle**, not a transfer:

1. **Pay** the factory in CNY.
2. **Clear** customs and pay duty/VAT.
3. **Prove** the import with invoices and declarations.
4. **Recover** VAT where possible.
5. **Finance** the gap until the marketplace pays.
6. **Trust** the factory to ship what was ordered.

Today these are split across a payment agency, a trade agency, a customs broker, a tax accountant, and a bank. Nobody owns the whole flow. The seller pays 6–11% for coordination, not for the money movement.

---

## 3. Solution

### 3.1 Product flow

```
1. Seller uploads PI (PDF/photo).
2. OCR extracts supplier, amount, HS code, Incoterm.
3. Quote engine returns landed cost: goods + FX + duty + VAT + FTA + logistics + inspection + credit.
4. Seller pays KRW (virtual account/card) and approves with passkey.
5. KR OpCo instructs TreasuryCo; factory receives CNY.
6. Document engine generates import declaration, tax invoice, VAT refund docs.
7. Seller tracks shipment and customs.
8. Credit line is available for the next order (30/60 days).
```

### 3.2 Product surfaces

**Seller (web/PWA)**
- Home: upcoming PIs, landed cost, cash runway.
- Quote: PI upload, cost breakdown, 10-minute FX lock.
- Checkout: KRW virtual account/card, passkey approval.
- Track: payment → production → shipping → customs → arrival.
- Documents: invoice, BL, import declaration, tax invoice.
- Credit: limit, draw, repay.

**Supplier (link/portal)**
- Invite link, KYB, bank account, export rights.
- Invoice confirmation, payout status, early payment.
- Performance score (on-time, quality, disputes).

**Ops/compliance console**
- Case queue: KYB, sanctions, TBML, disputes, payout failures.
- Payment timeline, document viewer, manual override with 4-eyes.
- Reconciliation: partner statement, bank, ledger.

**Partner API (Phase 2)**
- Quote, payment, document, webhook for trade agencies, 3PLs, marketplaces.

### 3.3 What the customer never sees

`USDC`, `wallet`, `gas`, `seed phrase`, `blockchain`. The customer sees KRW, landed cost, documents, and credit.

---

## 4. Pricing

| Line | Price | Notes |
|---|---|---|
| Payment + documents | 1.0–1.5% of GMV | Pure payment is 0.4% + FX (XTransfer); we don't compete there |
| Customs/tax SaaS | $100–300/month | or 0.2% of goods |
| Credit | 1.5–2.5%/month | the real margin |
| Supplier early payment | 1–2%/month | discount |

**Positioning:** the customer compares us to a 6–11% full-service agency, not to a 0.4% payment rail. Our all-in target is 2–4%.

---

## 5. Competition

| Player | Strength | Weakness | Our angle |
|---|---|---|---|
| XTransfer / PingPong | cheap payment, 200+ countries, licenses | no Korean customs/tax/credit | partner for the rail; own the trade ops |
| 1688 payment agencies | solve card block, order/pay | opaque, no API, no credit | transparency + data + credit |
| Trade agencies | full bundle, customs/logistics | 6–11%, manual, no credit | software + credit |
| Banks | trust, FX, compliance | no SME ops, no supplier onboarding | orchestrate the bank |
| Alibaba / 1688 | supply, Trade Assurance | no Korean landed cost/tax/credit | complement |
| VDX / Wavebridge | stablecoin infrastructure | export-side / institutional | partner or adjacent |

**Moat:** supplier graph + customs/tax data + credit underwriting + compliance operations. The payment rail is a commodity; the operating data is not.

---

## 6. Go-to-market summary

- **Supply-first:** sign 30–50 suppliers in one cluster (Guangzhou cosmetics packaging, Yiwu accessories) with a free receivables account and 24-hour payout.
- **Seller acquisition:** Naver Cafe/KakaoTalk seller communities, trade-agency partnerships, 3PL/customs broker referrals.
- **Sales script:** "Show me your last five payments. We'll quote your landed cost and your 30-day credit in 10 minutes."
- **Pilot:** 10 sellers, 30 payments, $500k GMV, zero losses, three repeat sellers.

Full plan: [GTM.md](GTM.md).

---

## 7. Metrics

| Metric | Target (Phase 1) |
|---|---:|
| GMV/month | $3M |
| Take rate | 2.0% |
| Gross margin after partner cost | 1.2%+ |
| Repeat purchase (60 days) | 40% |
| Loss rate | <0.3% |
| CAC payback | <6 months |
| Time-to-pay | <1 day after documents |
| Supplier NPS | >40 |

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| Korean FX/trade law | Trade agency/IoR structure; bank partner; legal opinion |
| China FX/crypto rules | HK MSO, export declaration, 外贸综服; no direct USDC to factory |
| AML/TBML | KYB, invoice matching, sanctions screening, case management |
| Credit loss | Small limits, insurance, funding partner, first-loss |
| Partner dependency | Multi-partner; fiat fallback |
| Incumbent response | Own the supplier graph and credit data; move faster on ops |
| Small ICP | Validate with 20 receipts and 30 interviews before scaling |

---

## 9. What we do not build

- Token, public-chain UX, or a consumer crypto app.
- A bank or VASP at launch; partner first.
- A marketplace; settle existing relationships.
- Balance-sheet lending; originate and service with a funding partner.
- All corridors at once; China first, then Vietnam, Mexico.

---

## 10. Why crypto, and why global

- **Crypto is the enabler, not the product.** Stablecoins give us one global treasury, 24/7 settlement, and programmable escrow. Without them, the model requires pre-funded bank accounts and correspondent banking in every corridor.
- **Global from day one.** The architecture is corridor-config driven. Korea → China is the first corridor; Vietnam, Mexico, Indonesia, and Turkey are configuration + partners, not a rewrite.
- **Invisible to the user.** The seller sees KRW; the factory sees local currency. No wallet, no gas, no seed phrase.

---

**KR 요약** — 첫 시장은 1688에서 사입하는 중형 한국 셀러다. 이들은 결제대행/무역대행에 2~11%를 내고, 랜딩 코스트·서류·신용을 한 곳에서 해결하지 못한다. Trade OS는 랜딩 코스트 체크아웃, 결제, 통관·세무, 공급사 신뢰, 30일 외상을 한 원장에 묶고, 동일한 아키텍처를 전 세계 SME 수입 corridor로 복제한다.
