#!/usr/bin/env python3
"""
Trade OS — runnable demo server (zero dependencies).

Run:
    python app/server.py
Then open:
    http://127.0.0.1:8000

This is a demo, not production. It uses SQLite, a fake payout, and no auth.
"""

import argparse
import json
import mimetypes
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.environ.get("TRADE_OS_DB", os.path.join(DATA_DIR, "trade_os.db"))


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def r2(value):
    return round(float(value) + 1e-9, 2)


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS quotes (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                goods_usd REAL NOT NULL,
                freight_usd REAL NOT NULL,
                fx_rate REAL NOT NULL,
                duty_rate REAL NOT NULL,
                vat_rate REAL NOT NULL,
                fee_rate REAL NOT NULL,
                credit_rate REAL NOT NULL,
                goods_krw REAL NOT NULL,
                freight_krw REAL NOT NULL,
                duty_krw REAL NOT NULL,
                vat_krw REAL NOT NULL,
                fee_krw REAL NOT NULL,
                credit_krw REAL NOT NULL,
                total_krw REAL NOT NULL,
                breakdown_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                quote_id TEXT NOT NULL,
                status TEXT NOT NULL,
                idempotency_key TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                funded_at TEXT,
                settled_at TEXT
            );

            CREATE TABLE IF NOT EXISTS ledger_entries (
                id TEXT PRIMARY KEY,
                payment_id TEXT,
                source_type TEXT NOT NULL,
                source_id TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ledger_postings (
                id TEXT PRIMARY KEY,
                entry_id TEXT NOT NULL,
                account TEXT NOT NULL,
                debit REAL NOT NULL DEFAULT 0,
                credit REAL NOT NULL DEFAULT 0,
                currency TEXT NOT NULL DEFAULT 'KRW'
            );
            """
        )
        conn.commit()


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def create_quote(payload):
    goods = float(payload.get("goods_usd", 10000))
    freight = float(payload.get("freight_usd", 500))
    fx = float(payload.get("fx_rate", 1350))
    duty_rate = float(payload.get("duty_rate", 0.08))
    vat_rate = float(payload.get("vat_rate", 0.10))
    fee_rate = float(payload.get("fee_rate", 0.018))
    credit_rate = float(payload.get("credit_rate", 0.015))

    if goods <= 0 or fx <= 0:
        raise ValueError("goods_usd and fx_rate must be positive")
    if freight < 0:
        raise ValueError("freight_usd must be zero or positive")

    goods_krw = r2(goods * fx)
    freight_krw = r2(freight * fx)
    cif_usd = goods + freight
    duty_usd = cif_usd * duty_rate
    vat_usd = (cif_usd + duty_usd) * vat_rate
    fee_usd = goods * fee_rate
    credit_usd = goods * credit_rate

    duty_krw = r2(duty_usd * fx)
    vat_krw = r2(vat_usd * fx)
    fee_krw = r2(fee_usd * fx)
    credit_krw = r2(credit_usd * fx)
    total_krw = r2(goods_krw + freight_krw + duty_krw + vat_krw + fee_krw + credit_krw)

    quote_id = "qte_" + uuid.uuid4().hex[:12]
    breakdown = {
        "goods_krw": goods_krw,
        "freight_insurance_krw": freight_krw,
        "duty_krw": duty_krw,
        "vat_krw": vat_krw,
        "platform_fee_krw": fee_krw,
        "credit_cost_krw": credit_krw,
    }
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO quotes (
                id, created_at, goods_usd, freight_usd, fx_rate, duty_rate,
                vat_rate, fee_rate, credit_rate, goods_krw, freight_krw,
                duty_krw, vat_krw, fee_krw, credit_krw, total_krw, breakdown_json
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                quote_id,
                now_iso(),
                goods,
                freight,
                fx,
                duty_rate,
                vat_rate,
                fee_rate,
                credit_rate,
                goods_krw,
                freight_krw,
                duty_krw,
                vat_krw,
                fee_krw,
                credit_krw,
                total_krw,
                json.dumps(breakdown),
            ),
        )
        conn.commit()
    return {
        "quote_id": quote_id,
        "fx_rate": fx,
        "breakdown": breakdown,
        "total_krw": total_krw,
        "expires_at": None,
    }


def create_payment(payload):
    quote_id = payload.get("quote_id")
    if not quote_id:
        raise ValueError("quote_id is required")
    idempotency_key = payload.get("idempotency_key") or ("idem_" + uuid.uuid4().hex[:16])
    with connect() as conn:
        existing = conn.execute(
            "SELECT * FROM payments WHERE idempotency_key = ?", (idempotency_key,)
        ).fetchone()
        if existing:
            return row_to_dict(existing)
        quote = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
        if not quote:
            raise ValueError("quote not found")
        payment_id = "pay_" + uuid.uuid4().hex[:12]
        conn.execute(
            "INSERT INTO payments (id, quote_id, status, idempotency_key, created_at) VALUES (?,?,?,?,?)",
            (payment_id, quote_id, "AWAITING_FUNDS", idempotency_key, now_iso()),
        )
        conn.commit()
        return {
            "payment_id": payment_id,
            "quote_id": quote_id,
            "status": "AWAITING_FUNDS",
            "idempotency_key": idempotency_key,
        }


def add_entry(conn, payment_id, postings):
    entry_id = "jrn_" + uuid.uuid4().hex[:12]
    conn.execute(
        "INSERT INTO ledger_entries (id, payment_id, source_type, source_id, created_at) VALUES (?,?,?,?,?)",
        (entry_id, payment_id, "payment", payment_id, now_iso()),
    )
    for account, debit, credit in postings:
        conn.execute(
            "INSERT INTO ledger_postings (id, entry_id, account, debit, credit, currency) VALUES (?,?,?,?,?,?)",
            ("pst_" + uuid.uuid4().hex[:12], entry_id, account, r2(debit), r2(credit), "KRW"),
        )
    return entry_id


def get_payment(payment_id):
    with connect() as conn:
        payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
        if not payment:
            raise ValueError("payment not found")
        quote = conn.execute("SELECT * FROM quotes WHERE id = ?", (payment["quote_id"],)).fetchone()
        entries = conn.execute(
            "SELECT * FROM ledger_entries WHERE payment_id = ? ORDER BY created_at", (payment_id,)
        ).fetchall()
        result_entries = []
        for entry in entries:
            postings = conn.execute(
                "SELECT account, debit, credit, currency FROM ledger_postings WHERE entry_id = ?",
                (entry["id"],),
            ).fetchall()
            result_entries.append(
                {
                    "entry_id": entry["id"],
                    "created_at": entry["created_at"],
                    "postings": [row_to_dict(p) for p in postings],
                }
            )
        return {
            "payment": row_to_dict(payment),
            "quote": row_to_dict(quote) if quote else None,
            "ledger": result_entries,
        }


def fund_payment(payment_id):
    with connect() as conn:
        payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()
        if not payment:
            raise ValueError("payment not found")
        if payment["status"] == "PAYOUT_SETTLED":
            return get_payment(payment_id)
        quote = conn.execute("SELECT * FROM quotes WHERE id = ?", (payment["quote_id"],)).fetchone()
        if not quote:
            raise ValueError("quote not found")

        total = quote["total_krw"]
        supplier = r2(quote["goods_krw"] + quote["freight_krw"])
        customs = r2(quote["duty_krw"] + quote["vat_krw"])
        platform_fee = r2(quote["fee_krw"] + quote["credit_krw"])

        if payment["status"] == "AWAITING_FUNDS":
            add_entry(
                conn,
                payment_id,
                [
                    ("client_cash", total, 0),
                    ("client_payable_seller", 0, total),
                ],
            )
            conn.execute(
                "UPDATE payments SET status = ?, funded_at = ? WHERE id = ?",
                ("FUNDS_RECEIVED", now_iso(), payment_id),
            )
            conn.commit()
            payment = conn.execute("SELECT * FROM payments WHERE id = ?", (payment_id,)).fetchone()

        if payment["status"] == "FUNDS_RECEIVED":
            add_entry(
                conn,
                payment_id,
                [
                    ("client_payable_seller", total, 0),
                    ("client_payable_supplier", 0, supplier),
                    ("client_payable_customs", 0, customs),
                    ("client_payable_platform_fee", 0, platform_fee),
                ],
            )
            add_entry(
                conn,
                payment_id,
                [
                    ("client_payable_supplier", supplier, 0),
                    ("client_cash", 0, supplier),
                ],
            )
            add_entry(
                conn,
                payment_id,
                [
                    ("client_payable_customs", customs, 0),
                    ("client_cash", 0, customs),
                ],
            )
            add_entry(
                conn,
                payment_id,
                [
                    ("client_payable_platform_fee", platform_fee, 0),
                    ("revenue", 0, platform_fee),
                ],
            )
            add_entry(
                conn,
                payment_id,
                [
                    ("operating_cash", platform_fee, 0),
                    ("client_cash", 0, platform_fee),
                ],
            )
            conn.execute(
                "UPDATE payments SET status = ?, settled_at = ? WHERE id = ?",
                ("PAYOUT_SETTLED", now_iso(), payment_id),
            )
            conn.commit()

    return get_payment(payment_id)


def ledger_summary():
    with connect() as conn:
        rows = conn.execute(
            "SELECT account, SUM(debit) AS debit, SUM(credit) AS credit FROM ledger_postings GROUP BY account ORDER BY account"
        ).fetchall()
        accounts = [row_to_dict(r) for r in rows]
        totals = conn.execute(
            "SELECT SUM(debit) AS debit, SUM(credit) AS credit FROM ledger_postings"
        ).fetchone()
        entries = conn.execute(
            "SELECT * FROM ledger_entries ORDER BY created_at"
        ).fetchall()
        result_entries = []
        for entry in entries:
            postings = conn.execute(
                "SELECT account, debit, credit, currency FROM ledger_postings WHERE entry_id = ?",
                (entry["id"],),
            ).fetchall()
            result_entries.append(
                {
                    "entry_id": entry["id"],
                    "payment_id": entry["payment_id"],
                    "created_at": entry["created_at"],
                    "postings": [row_to_dict(p) for p in postings],
                }
            )
        return {
            "accounts": accounts,
            "total_debit": r2(totals["debit"] or 0),
            "total_credit": r2(totals["credit"] or 0),
            "balanced": abs((totals["debit"] or 0) - (totals["credit"] or 0)) < 0.01,
            "entries": result_entries,
        }


def list_payments():
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, quote_id, status, created_at, funded_at, settled_at FROM payments ORDER BY created_at DESC LIMIT 50"
        ).fetchall()
        return [row_to_dict(r) for r in rows]


class Handler(BaseHTTPRequestHandler):
    server_version = "TradeOSDemo/1.0"

    def log_message(self, fmt, *args):
        print("[trade-os] " + fmt % args)

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _serve_file(self, path):
        if path == "/":
            path = "/static/index.html"
        if not path.startswith("/static/"):
            self.send_error(404, "Not found")
            return
        rel = path[len("/static/"):]
        full = os.path.abspath(os.path.join(STATIC_DIR, rel))
        if not full.startswith(STATIC_DIR + os.sep):
            self.send_error(403, "Forbidden")
            return
        if not os.path.isfile(full):
            self.send_error(404, "Not found")
            return
        mime, _ = mimetypes.guess_type(full)
        with open(full, "rb") as fh:
            body = fh.read()
        self.send_response(200)
        self.send_header("Content-Type", mime or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        try:
            if path == "/api/health":
                self._send_json(200, {"ok": True, "service": "trade-os-demo", "time": now_iso()})
            elif path == "/api/payments":
                self._send_json(200, {"payments": list_payments()})
            elif path.startswith("/api/payments/"):
                payment_id = path.split("/")[3]
                self._send_json(200, get_payment(payment_id))
            elif path == "/api/ledger":
                self._send_json(200, ledger_summary())
            else:
                self._serve_file(path)
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception as exc:  # demo: return a readable error
            self._send_json(500, {"error": type(exc).__name__ + ": " + str(exc)})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/quotes":
                self._send_json(201, create_quote(payload))
            elif path == "/api/payments":
                self._send_json(201, create_payment(payload))
            elif path.startswith("/api/payments/") and path.endswith("/fund"):
                payment_id = path.split("/")[3]
                self._send_json(200, fund_payment(payment_id))
            else:
                self.send_error(404, "Not found")
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception as exc:
            self._send_json(500, {"error": type(exc).__name__ + ": " + str(exc)})


def main():
    parser = argparse.ArgumentParser(description="Trade OS demo server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    args = parser.parse_args()
    init_db()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print("Trade OS demo running at http://%s:%d" % (args.host, args.port))
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
