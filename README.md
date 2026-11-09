# Trade OS

**The settlement and working-capital OS for Korea-origin cross-border trade.**

> A Korean seller uploads a factory invoice, sees the true landed cost, pays in one tap, and gets customs/tax documents plus 30-day credit. The factory receives local currency. Stablecoins are invisible plumbing.

## The problem

Korean SME importers buy from Chinese factories through a fragmented bundle: 1688 payment agencies (2–5%), trade agencies (6–11%), banks (slow, no credit), and gray brokers (illegal). Payment alone is commoditized — XTransfer already moves money at 0.4% + FX.

The unsolved parts are:
- **Landed-cost certainty**: duty, VAT, FTA, logistics, and credit are invisible until after the purchase.
- **Documents and compliance**: customs, tax invoices, VAT refunds, and supplier KYB are manual.
- **Working capital**: sellers pay upfront and wait 30–60 days for marketplace payouts.
- **Trust**: supplier fraud, quality disputes, and no recourse.

## The solution

Trade OS is the operating layer that binds five things into one ledger:

1. **Landed-cost checkout** — PI upload → duty/VAT/FTA/logistics/credit.
2. **One-tap payment** — KRW → CNY/VND/MXN through licensed partners.
3. **Documents, customs, tax** — invoice/BL/import declaration/tax invoice/VAT refund.
4. **Supplier trust** — KYB, milestone escrow, inspection, dispute.
5. **30/60-day credit** — underwritten by payment, customs, and marketplace data.

The customer never sees `USDC`, `wallet`, or `gas`. The factory never sees crypto. The Korean entity never touches crypto. Stablecoins are the settlement layer inside a licensed offshore treasury.

## Why now

- **Korea's FX law amendment (effective 2026-12-03)** brings cross-border crypto transfers into a registration and reporting regime. Legal rails exist, but only for licensed participants. Compliance becomes a moat.
- **Stablecoin B2B payment is validated** by XTransfer (1M+ business customers, $60B+ annual volume, 0.4% + FX for CNY payouts). The payment leg is commoditized; the trade-ops and credit layer is not.
- **1688 / Temu / AliExpress** have habituated Korean sellers to cross-border sourcing.
- **Korean e-commerce margin compression** creates demand for working capital.
- **AI agents** will procure and pay programmatically; the rail must be API-native.

## YC RFS fit

**"The Best Time to Build in Crypto"** — invisible stablecoin rails for real B2B trade, with revenue from day one and a compliance moat. This is not a token project. It is the operational layer that makes stablecoin B2B settlement work for a $50B trade flow.

## Repository map

- [docs/YC.md](docs/YC.md) — YC application narrative, RFS mapping, market, ask.
- [docs/PRODUCT.md](docs/PRODUCT.md) — customer, problem, solution, pricing, competition.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system architecture, money flow, ledger, legal structure.
- [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) — build plan, API, data model, sprints.
- [docs/GTM.md](docs/GTM.md) — beachhead, supply-first strategy, pilot.
- [docs/KR_SUMMARY.md](docs/KR_SUMMARY.md) — Korean translation summary.

## Status

Pre-seed. Architecture v1.0. One corridor: China → Korea. One vertical: 1688 K-beauty/accessories sellers. One wedge: landed cost + 30-day credit.

## Principles

1. Payments are a partner; we own documents, customs, tax, and credit.
2. The customer never sees crypto.
3. No document, no payment.
4. The Korean entity never touches crypto.
5. We do not make money on the payment spread; we make it on credit and software.

---

**KR 요약** — 한국 셀러가 1688 공장 PI를 올리면 랜딩 코스트를 확인하고, 1탭으로 결제·통관·세무·30일 외상까지 끝내는 B2B 무역 정산 OS. 결제는 파트너, 우리는 문서·통관·신용을 소유한다. 크립토는 백엔드 정산에만 존재한다.
