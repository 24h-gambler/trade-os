# Three-minute demo script

Run the demo locally:

```bash
python app/server.py
```

Open <http://127.0.0.1:8000>.

---

## 0:00–0:30 — The problem

> "A Korean seller buying from a Chinese factory pays 6–11% to a trade agency, waits for documents, and gets no credit. XTransfer already moves the money at 0.4% + FX. The payment is not the problem. The landed cost, the documents, and the credit are."

Show the **factory invoice** form.

## 0:30–1:00 — Landed cost

Enter:

- Goods: `10000`
- Freight: `500`
- FX: `1350`
- Duty: `8`
- VAT: `10`
- Fee: `1.8`
- Credit: `1.5`

Click **Calculate landed cost**.

> "The seller sees the all-in KRW cost before paying: goods, freight, duty, VAT, fee, and credit. This is the number they actually buy on."

Point at the total: **₩17,285,400**.

## 1:00–1:45 — Pay

Click **Pay in KRW**.

> "The seller pays KRW. The Korean entity instructs the offshore treasury. The factory receives local currency. The seller never sees USDC, a wallet, or gas."

Show the payment status: `AWAITING_FUNDS → FUNDS_RECEIVED → PAYOUT_SETTLED`.

## 1:45–2:30 — Ledger

Scroll to **Ledger**.

> "Every payment writes double-entry postings: client cash, supplier payable, customs payable, platform fee, revenue. The ledger balances to the won. This is the system of record that a payment app does not have."

Point at **Balanced** and the journal entries.

## 2:30–3:00 — Production and global

> "This demo is the core loop. Production adds KYB, sanctions, invoice matching, customs broker integration, 30-day credit, and partner adapters. The same architecture is corridor-config driven: Korea → China first, then Vietnam, Mexico, Indonesia, and beyond. Stablecoins are the reason it can settle globally at 24/7."

Close: **"Trade OS — landed cost, documents, and credit for global SME trade."**

---

## What to say if asked "is this real?"

- The demo uses a simulated payout, but the landed-cost math and double-entry ledger are real.
- The production architecture and partner plan are in [ARCHITECTURE.md](ARCHITECTURE.md) and [PLAN.md](PLAN.md).
- The first 90 days are a concierge pilot: 10 sellers, 30 payments, $500k GMV, zero losses.

## What not to say

- "We replace XTransfer." No — we partner for the rail.
- "We are a token." No — no token.
- "We can serve every country today." No — corridor by corridor.
