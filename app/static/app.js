const krw = new Intl.NumberFormat("ko-KR");

const $ = (id) => document.getElementById(id);

const els = {
  form: $("quote-form"),
  goods: $("goods"),
  freight: $("freight"),
  fx: $("fx"),
  duty: $("duty"),
  vat: $("vat"),
  fee: $("fee"),
  credit: $("credit"),
  error: $("error"),
  quoteEmpty: $("quote-empty"),
  quoteResult: $("quote-result"),
  total: $("total"),
  breakdown: $("breakdown"),
  pay: $("pay"),
  paymentStatus: $("payment-status"),
  balance: $("balance"),
  accounts: $("accounts"),
  entries: $("entries"),
};

let currentQuote = null;

function money(value) {
  return krw.format(Math.round(Number(value) || 0)) + "원";
}

function setError(message) {
  if (!message) {
    els.error.hidden = true;
    els.error.textContent = "";
    return;
  }
  els.error.hidden = false;
  els.error.textContent = message;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

function quotePayload() {
  return {
    goods_usd: Number(els.goods.value),
    freight_usd: Number(els.freight.value),
    fx_rate: Number(els.fx.value),
    duty_rate: Number(els.duty.value) / 100,
    vat_rate: Number(els.vat.value) / 100,
    fee_rate: Number(els.fee.value) / 100,
    credit_rate: Number(els.credit.value) / 100,
  };
}

function renderQuote(data) {
  currentQuote = data;
  const rows = [
    ["Goods", data.breakdown.goods_krw],
    ["Freight / insurance", data.breakdown.freight_insurance_krw],
    ["Duty", data.breakdown.duty_krw],
    ["VAT", data.breakdown.vat_krw],
    ["Platform fee", data.breakdown.platform_fee_krw],
    ["Credit cost", data.breakdown.credit_cost_krw],
  ];
  els.breakdown.innerHTML = rows
    .map(([label, value]) => `<tr><td>${label}</td><td>${money(value)}</td></tr>`)
    .join("");
  els.total.textContent = money(data.total_krw);
  els.quoteEmpty.hidden = true;
  els.quoteResult.hidden = false;
  els.paymentStatus.hidden = true;
  els.pay.disabled = false;
  els.pay.textContent = "Pay in KRW";
}

async function loadLedger() {
  const data = await api("/api/ledger");
  els.balance.textContent = data.balanced
    ? `Balanced · ${money(data.total_debit)}`
    : `UNBALANCED · Dr ${money(data.total_debit)} / Cr ${money(data.total_credit)}`;
  els.balance.classList.toggle("bad", !data.balanced);

  els.accounts.innerHTML = data.accounts
    .map(
      (row) =>
        `<tr><td>${row.account}</td><td class="num">${money(row.debit)}</td><td class="num">${money(
          row.credit
        )}</td></tr>`
    )
    .join("");

  if (!data.entries.length) {
    els.entries.innerHTML = `<div class="empty">No journal entries yet. Pay a quote.</div>`;
    return;
  }

  els.entries.innerHTML = data.entries
    .slice()
    .reverse()
    .map((entry) => {
      const postings = entry.postings
        .map(
          (p) =>
            `<tr><td>${p.account}</td><td>${money(p.debit)}</td><td>${money(p.credit)}</td></tr>`
        )
        .join("");
      return `
        <div class="entry">
          <div class="entry-head">
            <span>${entry.entry_id}</span>
            <span>${entry.payment_id || ""}</span>
          </div>
          <table>
            <thead><tr><th>Account</th><th>Debit</th><th>Credit</th></tr></thead>
            <tbody>${postings}</tbody>
          </table>
        </div>`;
    })
    .join("");
}

els.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setError("");
  els.pay.disabled = true;
  try {
    const data = await api("/api/quotes", {
      method: "POST",
      body: JSON.stringify(quotePayload()),
    });
    renderQuote(data);
  } catch (error) {
    setError(error.message);
  }
});

els.pay.addEventListener("click", async () => {
  if (!currentQuote) return;
  setError("");
  els.pay.disabled = true;
  els.pay.textContent = "Processing...";
  try {
    const idempotencyKey =
      (crypto.randomUUID && crypto.randomUUID()) || "idem_" + Date.now();
    const payment = await api("/api/payments", {
      method: "POST",
      body: JSON.stringify({
        quote_id: currentQuote.quote_id,
        idempotency_key: idempotencyKey,
      }),
    });
    const funded = await api(`/api/payments/${payment.payment_id}/fund`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    const status = funded.payment.status;
    els.paymentStatus.hidden = false;
    els.paymentStatus.textContent = `${payment.payment_id} · ${status} · ${money(
      funded.quote.total_krw
    )} settled`;
    els.pay.textContent = "Paid";
    await loadLedger();
  } catch (error) {
    setError(error.message);
    els.pay.disabled = false;
    els.pay.textContent = "Pay in KRW";
  }
});

loadLedger().catch((error) => setError(error.message));
