# Trade OS — runnable demo

Zero dependencies. Python 3.11+.

## Run

```bash
python app/server.py
```

Open <http://127.0.0.1:8000>.

## Demo flow

1. Enter a factory invoice: goods $10,000, freight $500, FX 1,350, duty 8%, VAT 10%, fee 1.8%, credit 1.5%.
2. Click **Calculate landed cost**. The server returns the all-in KRW cost.
3. Click **Pay in KRW**. The server creates a payment, simulates funding and payout, and writes double-entry ledger postings.
4. Scroll to **Ledger**. Check that total debits equal total credits.

## API

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | health check |
| POST | `/api/quotes` | create landed-cost quote |
| POST | `/api/payments` | create payment from quote |
| POST | `/api/payments/{id}/fund` | simulate funding + payout + ledger |
| GET | `/api/payments/{id}` | payment + ledger |
| GET | `/api/ledger` | ledger summary + entries |
| GET | `/api/payments` | recent payments |

### Quote request

```json
{
  "goods_usd": 10000,
  "freight_usd": 500,
  "fx_rate": 1350,
  "duty_rate": 0.08,
  "vat_rate": 0.10,
  "fee_rate": 0.018,
  "credit_rate": 0.015
}
```

### Payment + fund

```bash
curl -X POST http://127.0.0.1:8000/api/payments \
  -H "Content-Type: application/json" \
  -d '{"quote_id":"qte_...","idempotency_key":"demo-1"}'

curl -X POST http://127.0.0.1:8000/api/payments/pay_.../fund \
  -H "Content-Type: application/json" -d '{}'
```

## Smoke test

```bash
python scripts/smoke_test.py
```

Starts the server on port 8011 with a temporary database, runs quote → payment → fund → ledger, and asserts that the ledger balances.

## What this demonstrates

- Landed-cost calculation: goods, freight, duty, VAT, fee, credit.
- Payment state machine: `AWAITING_FUNDS → FUNDS_RECEIVED → PAYOUT_SETTLED`.
- Double-entry ledger: client cash vs operating cash, payables, revenue.
- Idempotent payment creation.

## What it does not do

- No real money, no real bank/PSP/VASP.
- No auth, KYC, sanctions, customs filing.
- No credit underwriting.
- SQLite, not Postgres.

This is a demo for YC and partner conversations. The production architecture is in [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).
