# Trade OS

**The settlement and working-capital OS for Korea-origin cross-border trade.**

> A Korean seller uploads a factory invoice, sees the true landed cost, pays in one tap, and gets customs/tax documents plus 30-day credit. The factory receives local currency. Stablecoins are invisible plumbing.

**Two-line summary** Trade OS is the settlement and working-capital OS for Korea-origin cross-border trade, starting with 1688 sellers. Stablecoin rails make it globally replicable: one treasury, 24/7 settlement, and local payout in any corridor — without correspondent banking.

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

## Why crypto, and why global

Stablecoins are not a feature. They are the reason this model works at global scale.

- **One global treasury, not a bank account per corridor.** TreasuryCo holds USDC and pays local partners in CNY, VND, MXN, or any other currency. A traditional trade agency would need pre-funded bank accounts, correspondent banking, and 3–5 day wires in every country.
- **24/7 settlement.** Factories get paid on weekends and holidays; sellers do not wait for bank cut-offs.
- **Programmable money.** Escrow, milestone release, and supplier early payment are code, not manual instructions.
- **Global from day one.** The architecture is corridor-config driven: currency, partners, tax rules, and documents are data, not code. Korea → China is the beachhead, not the ceiling. The same stack replicates to Vietnam, Mexico, Indonesia, Turkey, and beyond.
- **Invisible to the customer.** The seller sees KRW; the factory sees local currency. No wallet, no gas, no seed phrase.

This is the YC crypto problem: not a token, but the invisible rail that lets real B2B trade settle globally in real time.

## YC RFS fit

**"The Best Time to Build in Crypto"** — invisible stablecoin rails for real B2B trade, with revenue from day one and a compliance moat. This is not a token project. It is the operational layer that makes stablecoin B2B settlement work for a $50B trade flow, and it is globally replicable corridor by corridor.

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

**KR 두 줄 요약** — Trade OS는 한국 셀러의 1688 사입 대금을 랜딩 코스트·통관·세무·30일 외상까지 한 원장에서 처리하는 B2B 무역 정산 OS다. 스테이블코인 기반의 글로벌 정산 레일 덕분에, 한국-중국을 시작으로 전 세계 어느 corridor에서도 24/7 즉시 정산이 가능하다.
