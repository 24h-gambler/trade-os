# YC Application Narrative

**Company** Trade OS  
**One-liner** The settlement and working-capital OS for Korea-origin cross-border trade.  
**RFS** The Best Time to Build in Crypto (invisible stablecoin B2B rails).

---

## 1. What are you building?

A Korean seller uploads a factory invoice (PI) in our app. We show the **true landed cost** — goods, FX, duty, VAT, FTA, logistics, inspection, and credit. The seller pays in KRW in one tap. The Chinese factory receives CNY. We generate the import declaration, tax invoice, and VAT refund documents, and extend 30/60-day credit to the seller.

The customer never sees crypto. The factory never sees crypto. The Korean entity never touches crypto. Stablecoins settle inside a licensed offshore treasury.

**In one sentence:** Stripe for Korea-origin trade — but the product is not the payment. The product is the landed cost, the documents, and the credit.

---

## 2. The problem

Korean SME importers buy from Chinese factories through a fragmented, opaque bundle:

| Path | Cost | Time | Documents | Credit |
|---|---:|---|---|---|
| 1688 payment agency (payment only) | 2–5% | 1–3 days | optional invoice | none |
| 1688 full service (inspection/customs/delivery) | **6–11%** | 2–5 days | agency | some |
| Bank T/T | 1.5–3% + fee | 1–3 days (new supplier 1–3 weeks) | seller's job | none |
| Trade agency | 3–11% | 2–5 days | agency | some |
| Gray broker / underground remittance | 1.5–3% + risk | 1–3 days | none | none |
| XTransfer | 0.4% + FX | 1–3 days | none | none |

**Payments are already commoditized.** XTransfer alone has 1M+ business customers, $60B+ annual volume, and charges 0.4% + FX for CNY payouts. A "cheaper USDC transfer" is not a company.

**The unsolved problems are:**
1. **Landed-cost uncertainty** — the seller does not know the all-in cost until after customs.
2. **Documents and compliance** — customs, tax invoices, VAT refunds, and supplier KYB are manual.
3. **Working capital** — the seller pays upfront and waits 30–60 days for Coupang/Amazon payouts.
4. **Trust** — supplier fraud, quality disputes, and no recourse.

The seller is not buying a transfer. They are buying a bundle: *the goods arrive, the documents are right, and cash keeps moving.*

---

## 3. Why existing solutions fail

- **Banks** are legal and cheap for simple wires, but they do not onboard suppliers, handle small-ticket trade documents, or extend credit to SMEs.
- **Trade agencies** bundle the work but charge 6–11%, are opaque, and have no data or credit product.
- **XTransfer / PingPong** are excellent payment rails, but they are built around Chinese exporters and do not own Korean import customs, tax, or credit.
- **1688 payment agencies** solve the "Korean card is blocked" problem, but they are order-takers, not a settlement system of record.
- **Alibaba / 1688 Trade Assurance** covers the transaction, not the Korean landed cost, tax, or working capital.

The gap is not the rail. The gap is the **operating layer** that binds the rail to documents, customs, tax, and credit.

---

## 4. The solution

### 4.1 Five modules, one ledger

| Module | What the customer sees | What we own |
|---|---|---|
| **Landed-cost checkout** | PI upload → all-in KRW cost | quote snapshot, HS/FTA/VAT engine |
| **One-tap payment** | KRW → factory's local currency | orchestration, partner routing, state machine |
| **Documents / customs / tax** | invoice, BL, import declaration, tax invoice | document matching, broker integration, VAT refund |
| **Supplier trust** | KYB, escrow, inspection, dispute | supplier graph, performance/dispute history |
| **Credit** | 30/60-day terms, early payout | underwriting, funding partner, collections |

### 4.2 The wedge

**One corridor: China → Korea. One vertical: 1688 K-beauty/accessories sellers. One wedge: landed cost + 30-day credit.**

We are not building a global trade marketplace. We are building the sharpest tool for a seller who already buys from 1688, already pays 6–11%, and cannot get credit.

### 4.3 The money flow

```
Seller → KRW → PG client account → KR OpCo (trade agency / importer of record)
KR OpCo → intercompany → TreasuryCo (SG/HK, USDC)
TreasuryCo → CNY → Chinese factory (via HK MSO)
KR OpCo → import declaration → customs → tax invoice
```

- The Korean entity never holds crypto.
- The offshore treasury holds USDC and settles with licensed partners.
- Client funds are segregated; the platform instructs, but does not custody.
- The ledger is double-entry, multi-currency, and reconciled daily.

---

## 5. Why now

1. **Regulatory clarity.** Korea's FX law amendment takes effect on 2026-12-03. Cross-border crypto transfers become a registered "virtual asset transfer business" with reporting to the authorities. This is not a free-for-all; it is a licensed regime. That is good for a compliance-native operator and bad for gray brokers.
2. **Payment commoditization.** XTransfer at 0.4% + FX proves the rail is cheap. The value has moved to trade operations and credit.
3. **Sourcing habit.** 1688, Temu, and AliExpress have trained Korean sellers to buy directly from Chinese factories.
4. **Margin pressure.** Korean e-commerce margins are thin; 30/60-day credit is a survival tool, not a luxury.
5. **Agentic commerce.** AI agents will read PIs, compare landed costs, and pay suppliers. The rail must be API-native.

---

## 6. Why us

- **Domain:** we have operated trade agency, customs, and payment workflows. We know where the 6–11% goes.
- **Supplier network:** we start supply-first in one cluster (e.g., Guangzhou cosmetics packaging, Yiwu accessories), signing 30–50 suppliers before scaling sellers.
- **Concierge traction plan:** 90 days, 10 sellers, 30 payments, $500k GMV, zero losses.
- **Not a crypto team:** stablecoins are plumbing. We are a trade-ops and credit team.

---

## 7. Market

- Korea SME import flow: **~$50B** (estimate).
- 5% share = **$2.5B GMV** → **$30–50M revenue** at a 1.3–1.8% blended take.
- $1B GMV ≈ **$15–20M revenue**.
- $100M ARR requires **$5–6B GMV** or 50%+ credit penetration.
- Expansion: Japan, Taiwan, Singapore, Vietnam, Mexico → 3x the pool.

The market is not "all cross-border payments." It is the **small-ticket, document-heavy, credit-starved** segment that banks and payment rails do not serve.

---

## 8. Business model

| Revenue line | Price | Note |
|---|---|---|
| Payment + documents | 1.0–1.5% of GMV | We do not compete with XTransfer on the pure rail |
| Customs/tax SaaS | $100–300/month | or 0.2% of goods |
| **Credit** | **1.5–2.5%/month** | the real margin |
| Supplier early payment | 1–2%/month | discount |

**We do not make money on the payment spread. We make it on credit and software.**

Unit economics (example): $32k monthly GMV per customer; payment GM $320; credit $144; SaaS $50; total contribution $514/month; CAC $2,000; payback 3.9 months.

---

## 9. Competition and moat

| Player | What they solve | What they do not |
|---|---|---|
| XTransfer / PingPong | payment, FX, local payout | Korean customs, tax, credit, supplier trust |
| 1688 payment agencies | order + payment | transparency, API, credit |
| Trade agencies | full bundle | 6–11% cost, no data, no credit |
| Banks | trust, FX, compliance | SME operations, documents, credit |
| Alibaba / 1688 | supply + Trade Assurance | Korean landed cost, tax, credit |
| VDX / Wavebridge | stablecoin infrastructure | Korean buyer-side trade OS |

**Moat:** supplier graph (KYB, accounts, performance, disputes) + customs/tax operating data + credit underwriting + compliance operations. The rail is a partner; the data and credit are ours.

---

## 10. 90-day plan

| Week | Milestone | Pass criteria |
|---|---|---|
| 1–2 | 30 seller interviews; 10 supplier interviews; 5 quotes | median all-in 3%+ / 5 days+ |
| 3–4 | Legal opinion: trade agency/IoR, FX, VASP partner | structure viable |
| 5–8 | Concierge pilot: 10 sellers, 30 payments | $500k GMV, 0 losses |
| 9–10 | Supplier cluster: 30 suppliers onboarded | 10 active |
| 11–12 | Credit pilot with 3 sellers | 30-day terms, 0 default |
| 13 | Decide: seed raise or extend concierge | 3 repeat sellers |

**Kill criteria:** median all-in cost <2%; 4% payers are mostly tax evaders; suppliers refuse third-party payout; compliance cost >1%; CAC payback >9 months.

---

## 11. Ask

**$500k–1M pre-seed** (or YC's $500k) for 12–18 months:

- 2 engineers, 1 operations/compliance lead, 1 supplier-network lead.
- Legal: trade/FX/customs/tax opinions.
- Partner integrations: bank/PG, HK MSO, customs broker, credit funder.
- Pilot: 50 sellers, $3M/month GMV, 1 corridor, credit pilot, zero losses.

---

## 12. What we are not

- Not a token project.
- Not a wallet or a consumer crypto app.
- Not a bank or a VASP at launch; we partner first.
- Not a marketplace; we settle existing buyer-supplier relationships.
- Not a balance-sheet lender; we originate and service, a funding partner provides capital.
- Not a global trade platform; one corridor, one vertical, one wedge.

---

## 13. Ten-slide narrative

1. **Title** — Stripe for Korea-origin trade. The product is landed cost, documents, and credit.
2. **Problem** — 6–11% opaque bundle; 30–60 day cash gap; no credit.
3. **Why now** — FX law registration (2026-12-03), payment commoditization, 1688 habit, margin pressure.
4. **Solution** — landed-cost checkout + one-tap payment + customs/tax + 30-day credit.
5. **Demo** — PI upload → landed cost → pay → factory CNY → import declaration/tax invoice → credit line.
6. **Market** — $50B flow; 5% = $2.5B GMV; $30–50M revenue; Japan/SEA 3x.
7. **Business model** — 1.0–1.5% payment/docs + 1.5–2.5%/month credit + SaaS.
8. **Traction plan** — 10 sellers, $500k GMV, 0 losses, 3 suppliers, 1 credit pilot.
9. **Competition** — XTransfer, trade agencies, banks, VDX; moat = supplier graph + customs/tax data + credit.
10. **Team/ask** — domain expertise, 90-day plan, $500k–1M.

---

**KR 요약** — 한국 셀러의 1688 사입 대금을 랜딩 코스트·통관·세무·30일 외상까지 한 원장에서 처리하는 Trade OS. 결제는 XTransfer/은행/VASP 파트너, 우리는 문서·통관·신용을 소유한다. 크립토는 백엔드 정산에만 존재한다.
