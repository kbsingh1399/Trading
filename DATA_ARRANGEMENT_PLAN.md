# Arranging the Missing Data to Check the Papers' Hypotheses

*Asked: obtain the data the papers need so their hypotheses can be checked.
This document records (1) exactly what I attempted and what this sandbox can and
cannot reach, (2) the precise missing dataset per paper family with the exact
source to obtain it, and (3) which families are already fully tested on data we
have. It is a shopping list plus a feasibility report, not a promise.*

---

## 1. What this sandbox can reach (verified this turn)

| endpoint | status |
|---|---|
| `github.com` (git push/clone, API) | **reachable** |
| `api.github.com` | reachable (search returned empty) |
| `data.binance.vision` | **blocked** |
| `api.binance.com` | **blocked** |
| `public.bybit.com` | **blocked** |
| `raw.githubusercontent.com`, `codeload`, `archive.org`, `zenodo.org` | **blocked** |

**Consequence:** I cannot download exchange L2 archives, vendor feeds, or public
dataset dumps from this sandbox. Every serious L2 source is either on a blocked
host or requires a paid / whitelisted account. So *true* order-book data cannot
be arranged here; it must be obtained outside and handed to this workspace.

---

## 2. Missing data per paper family, source, and what it unlocks

| family (count) | example hypothesis | missing data | source | feasible here? |
|---|---|---|---|---|
| Order Book Microstructure (96) | spread/depth imbalance, microprice (Felder), Tapiero depth | tick / L2 snapshots | Binance futures `S_Depth`/`T_Depth` (whitelisted acct) or **Tardis.dev** `incremental_book_L2` (BTCUSDT from 2019-12-01, paid) | NO |
| ML / DeepLOB (89) | LOB-image predictors | L2 snapshots | same as above | NO |
| OFI trade imbalance (219) | multi-level OFI (Cont) | L2 + trades | same; trades via Binance `aggTrades` (blocked) | NO |
| Perpetual funding & carry (270) | funding/basis carry | funding (HAVE), basis (HAVE) | already in 15m masters | **YES — tested** |
| Liquidation cascades (39) | liq absorption | liq columns (HAVE) | already in 15m masters | **YES — tested** |
| Vol forecasting (21) | vol-targeting | returns (HAVE) | already in 15m masters | **YES — tested** |
| Volume profiles (6) | intraday breakout | volume (HAVE) | already in 15m masters | **YES — tested** |

The **~404 papers needing L2** (96+89+~219) are the only untestable block, and
their data is not obtainable in this sandbox.

### The one reportedly-public processed-L2 dataset
ssrn-6344338 (Rajendran & Singaravelu) is *claimed* (forum report, **unverified**)
to distribute ~1 year of processed L2 features as CSV from its SSRN page. If real,
it would unlock the microstructure families without raw book data. It would need
to be downloaded outside this sandbox (SSRN page) and dropped into the workspace.

---

## 3. What is already fully tested (data we have)

Every family whose data exists in the 15m masters has been tested under the
familywise-corrected protocol, with the results in `EDGE_SYSTEM.md`,
`HYPOTHESIS_BATTERY.md`, and the scratch test files:

- 32-hypothesis battery (trend veto, entry, exit, sizing): **0 survive Holm**
- 8 orderflow gates: **1** (whale activity) survives Holm but **decays** (2026 −0.187)
- walk-forward exit geometry: **break-even ceiling** (oracle best −0.0068)
- daily cross-sectional orderflow: +9.6 bps/d vs 82 bps/d cost — **dies**
- weekly low-turnover cross-section: +0.83%/wk t=1.62, fails 2025/26 — **no**
- funding carry (270): +0.026%/d t=0.41 — **no** (after fixing a 32× aggregation bug)

So the trade-level families are exhausted; only L2 remains, and it is blocked.

---

## 4. What to obtain (for someone with real network/accounts)

Priority order, cheapest first:

1. **ssrn-6344338 processed L2 CSV** (if it exists) — unlocks microstructure tests
   with no vendor account. Verify on the SSRN page; download; place in `scratch/`.
2. **Tardis.dev** Binance spot `incremental_book_L2`, BTCUSDT, from 2019-12-01 —
   paid, but the cleanest path to test Felder microprice / depth imbalance.
3. **Binance futures** `S_Depth`/`T_Depth` via `/sapi/v1/futuresHistDataId` —
   requires a whitelisted futures account; from Jan 2020.
4. Do **not** build on `data.binance.vision` bookTicker — it is stale (last
   update ~2024) and has no historical-depth API.

Once any of these lands in the workspace, I will run the microstructure battery
(spread, depth imbalance, microprice, multi-level OFI) as selection gates on the
improved T1 geometry under the same corrected protocol.

---

## 5. Honest expectation

Even with L2, the binding constraint has been cost, not signal: every tested
edge sits below 41 bps. Microstructure signals typically help *execution*
(when/where to post) more than *direction*. So L2 is most likely to close the
**1.4 bps** gap via better fills, not to create a new directional edge. That is
still the single highest-value use of new data — and it is precisely the gap
between "no edge" and "edge" for the one real signal in this repository (T1).
