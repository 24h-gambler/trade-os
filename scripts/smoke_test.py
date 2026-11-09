#!/usr/bin/env python3
"""Smoke test for the Trade OS demo.

Starts the server on a test port with a temporary SQLite database,
runs quote -> payment -> fund -> ledger, and asserts the ledger balances.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8011
BASE = "http://127.0.0.1:%d" % PORT


def request(method, path, payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    db_path = os.path.join(tempfile.gettempdir(), "trade_os_smoke_%d.db" % os.getpid())
    if os.path.exists(db_path):
        os.remove(db_path)

    env = os.environ.copy()
    env["TRADE_OS_DB"] = db_path
    server = os.path.join(ROOT, "app", "server.py")
    proc = subprocess.Popen(
        [sys.executable, server, "--port", str(PORT)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        for _ in range(40):
            try:
                if request("GET", "/api/health").get("ok"):
                    break
            except Exception:
                time.sleep(0.25)
        else:
            raise RuntimeError("server did not start on port %d" % PORT)

        quote = request(
            "POST",
            "/api/quotes",
            {
                "goods_usd": 10000,
                "freight_usd": 500,
                "fx_rate": 1350,
                "duty_rate": 0.08,
                "vat_rate": 0.10,
                "fee_rate": 0.018,
                "credit_rate": 0.015,
            },
        )
        assert quote["total_krw"] > 0, quote
        assert quote["breakdown"]["duty_krw"] > 0, quote
        assert quote["breakdown"]["vat_krw"] > 0, quote

        payment = request(
            "POST",
            "/api/payments",
            {"quote_id": quote["quote_id"], "idempotency_key": "smoke-1"},
        )
        assert payment["status"] == "AWAITING_FUNDS", payment

        funded = request("POST", "/api/payments/%s/fund" % payment["payment_id"], {})
        assert funded["payment"]["status"] == "PAYOUT_SETTLED", funded["payment"]

        ledger = request("GET", "/api/ledger")
        assert ledger["balanced"], ledger
        assert abs(ledger["total_debit"] - ledger["total_credit"]) < 0.01, ledger

        print("PASS")
        print("quote=%s total_krw=%s" % (quote["quote_id"], quote["total_krw"]))
        print("payment=%s status=%s" % (payment["payment_id"], funded["payment"]["status"]))
        print(
            "ledger debit=%s credit=%s balanced=%s"
            % (ledger["total_debit"], ledger["total_credit"], ledger["balanced"])
        )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == "__main__":
    main()
