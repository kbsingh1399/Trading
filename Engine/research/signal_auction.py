"""
================================================================================
ENGINE RESEARCH: REAL-TIME SIGNAL AUCTION ENGINE (GATE 2 — OPPORTUNITY ARBITRATION)
================================================================================
PURPOSE:
    Per-bar signal arbitration that:
    1. Reads the approved_pool.json written by asset_screener.py (Gate 1).
    2. Receives candidate signals from the live inference engine.
    3. Ranks them by a composite Expected Value score.
    4. Enforces correlation cluster firewall (max 1 per cluster).
    5. Awards open position slots to the top-ranked eligible assets.

RANKING FORMULA (Expected Value Score):
    EV = P_win * win_R - (1 - P_win) * loss_R
    Quality_Factor = 1 / max(spread_atr_ratio, 0.01)
    Calmar_Factor  = min(asset_calmar / 20.0, 3.0)    -- normalized, capped
    Score = EV * Quality_Factor * Calmar_Factor

ANTI-GAMING GUARANTEE:
    - Calmar_Factor comes ONLY from Gate 1 (historical training data).
    - Live probs are the ONLY real-time component.
    - No look-ahead: spread/ATR taken from the current closed 15m bar only.

INTEGRATION:
    Import AuctionEngine and call .rank_signals(candidate_list) each bar.
    candidate_list is a list of SignalCandidate dicts from inference_engine.py.
================================================================================
"""
import json, logging, os, sys
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set
from datetime import datetime, timezone

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

APPROVED_POOL_PATH = os.path.join(SCRIPT_DIR, 'approved_pool.json')

log = logging.getLogger('SignalAuction')


# ─── DATA STRUCTURES ────────────────────────────────────────────────────────

@dataclass
class SignalCandidate:
    symbol: str
    direction: str             # 'BUY' or 'SELL'
    prob_win: float            # XGBoost P*(win) in [0, 1]
    spread_atr_ratio: float    # spread / atr_14 (from latest 15m bar)
    atr_14: float              # ATR in price units (for SL sizing)
    bar_time: datetime         # UTC timestamp of the triggering bar

    # Optional enrichment (filled by AuctionEngine)
    ev_score: float = 0.0
    calmar_factor: float = 1.0
    quality_factor: float = 1.0
    composite_score: float = 0.0
    cluster: Optional[str] = None
    admitted: bool = False
    veto_reason: Optional[str] = None


@dataclass
class AuctionResult:
    admitted: List[SignalCandidate]
    vetoed: List[SignalCandidate]
    bar_time: datetime
    open_slots: int
    pool_size: int


# ─── CORRELATION CLUSTERS ────────────────────────────────────────────────────

CORRELATION_CLUSTERS: Dict[str, Set[str]] = {
    'EUR_BLOC':       {'EURUSD', 'EURSEK', 'EURCNH', 'EURHUF', 'EURAUD', 'EURCAD',
                       'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURSGD', 'EURMXN',
                       'EURNOK', 'EURHKD', 'EURZAR'},
    'USD_BLOC':       {'NZDUSD', 'AUDCHF', 'AUDUSD', 'GBPUSD', 'USDCAD', 'USDJPY',
                       'USDSGD', 'USDCNH', 'USDSEK', 'USDHKD', 'USDMXN', 'USDNOK',
                       'USDZAR', 'USDCZK', 'USDDKK', 'USDHUF', 'USDPLN', 'USDRUB'},
    'CNH_BLOC':       {'NZDCNH', 'XAUCNH', 'GAUCNH', 'AUDCNH', 'GBPCNH', 'CNHJPY'},
    'INDEX_BLOC':     {'GER40', 'GER30', 'FR40', 'AU200', 'US2000', 'DJ30', 'SP500',
                       'NAS100', 'CHINA50', 'CHINAH', 'UK100'},
    'COMMODITY_BLOC': {'GAS', 'NICKEL', 'LEAD', 'COPPER', 'ALUMINIUM', 'GAUUSD', 'XAUUSD', 'XAGUSD'},
    'AUD_BLOC':       {'AUDJPY', 'AUDNZD', 'AUDSGD', 'AUDCAD'},
    'GBP_BLOC':       {'GBPJPY', 'GBPNZD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPSGD',
                       'GBPNOK', 'GBPSEK', 'GBPHKD'},
}

WIN_R  = 2.5   # matches strategy target
LOSS_R = 1.0   # full stop-out = 1R


def _get_cluster(symbol: str) -> Optional[str]:
    sym = symbol.upper().replace('.PI', '').replace('.P', '').replace('.R', '')
    for c_name, members in CORRELATION_CLUSTERS.items():
        if sym in members:
            return c_name
    return None


# ─── APPROVED POOL LOADER ────────────────────────────────────────────────────

class ApprovedPool:
    """
    Reads and caches approved_pool.json written by Gate 1 screener.
    Provides O(1) lookups for calmar scores and membership checks.
    """
    def __init__(self, pool_path: str = APPROVED_POOL_PATH):
        self.path = pool_path
        self._pool: Dict[str, Dict] = {}
        self._generated_at: Optional[str] = None
        self.reload()

    def reload(self):
        if not os.path.exists(self.path):
            log.warning(f'approved_pool.json not found at {self.path}. Pool is EMPTY — run asset_screener.py first.')
            self._pool = {}
            return
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._generated_at = data.get('generated_at', 'unknown')
        self._pool = {a['symbol']: a for a in data.get('assets', [])}
        log.info(f'ApprovedPool loaded: {len(self._pool)} assets (generated {self._generated_at})')

    def is_approved(self, symbol: str) -> bool:
        return symbol.upper().replace('.PI','').replace('.P','').replace('.R','') in self._pool

    def get_calmar(self, symbol: str) -> float:
        sym = symbol.upper().replace('.PI','').replace('.P','').replace('.R','')
        return self._pool.get(sym, {}).get('calmar', 1.0)

    def symbols(self) -> List[str]:
        return list(self._pool.keys())

    def __len__(self): return len(self._pool)


# ─── AUCTION ENGINE ──────────────────────────────────────────────────────────

class AuctionEngine:
    """
    Real-time per-bar signal arbitration engine.

    Usage:
        engine = AuctionEngine(max_slots=3)
        result = engine.rank_signals(candidates, open_symbols={'EURUSD'})
        for sig in result.admitted:
            place_order(sig.symbol, sig.direction)
    """
    def __init__(self, max_slots: int = 3, pool_path: str = APPROVED_POOL_PATH):
        self.max_slots = max_slots
        self.pool = ApprovedPool(pool_path)
        log.info(f'AuctionEngine ready | max_slots={max_slots} | pool={len(self.pool)} assets')

    def reload_pool(self):
        """Call this after running asset_screener.py to refresh the pool."""
        self.pool.reload()

    def _compute_ev(self, prob_win: float) -> float:
        return prob_win * WIN_R - (1 - prob_win) * LOSS_R

    def _compute_composite_score(self, candidate: SignalCandidate) -> float:
        ev = self._compute_ev(candidate.prob_win)
        if ev <= 0:
            return -999.0  # negative EV always vetoed
        quality_factor = 1.0 / max(candidate.spread_atr_ratio, 0.005)
        calmar = self.pool.get_calmar(candidate.symbol)
        calmar_factor = min(calmar / 20.0, 3.0)  # normalized, capped at 3x bonus
        return ev * quality_factor * calmar_factor

    def rank_signals(
        self,
        candidates: List[SignalCandidate],
        open_symbols: Optional[Set[str]] = None
    ) -> AuctionResult:
        """
        Core auction logic:
        1. Filter out non-approved and duplicate symbols.
        2. Score all surviving candidates.
        3. Sort by composite score descending.
        4. Greedily award slots enforcing cluster firewall.

        Args:
            candidates:    List of SignalCandidate from inference engines this bar.
            open_symbols:  Set of symbols already in open positions (to block duplicates).
        Returns:
            AuctionResult with admitted and vetoed candidates.
        """
        if open_symbols is None:
            open_symbols = set()

        bar_time = candidates[0].bar_time if candidates else datetime.now(timezone.utc)
        open_slots = max(0, self.max_slots - len(open_symbols))
        admitted: List[SignalCandidate] = []
        vetoed: List[SignalCandidate] = []
        used_clusters: Set[str] = set()

        # ── Pre-filter ───────────────────────────────────────────────────
        scored = []
        for cand in candidates:
            sym = cand.symbol.upper().replace('.PI','').replace('.P','').replace('.R','')

            # Gate 2a: Must be in approved pool
            if not self.pool.is_approved(sym):
                cand.admitted = False
                cand.veto_reason = 'Not in approved pool'
                vetoed.append(cand)
                continue

            # Gate 2b: No duplicate open position
            if sym in {s.upper().replace('.PI','').replace('.P','').replace('.R','') for s in open_symbols}:
                cand.admitted = False
                cand.veto_reason = 'Duplicate open position'
                vetoed.append(cand)
                continue

            # Score surviving candidates
            cand.cluster = _get_cluster(sym)
            cand.quality_factor = 1.0 / max(cand.spread_atr_ratio, 0.005)
            cand.calmar_factor = min(self.pool.get_calmar(sym) / 20.0, 3.0)
            cand.ev_score = self._compute_ev(cand.prob_win)
            cand.composite_score = self._compute_composite_score(cand)
            scored.append(cand)

        # ── Sort by score descending ──────────────────────────────────────
        scored.sort(key=lambda x: x.composite_score, reverse=True)

        # ── Greedy slot award ─────────────────────────────────────────────
        for cand in scored:
            if len(admitted) >= open_slots:
                cand.admitted = False
                cand.veto_reason = 'No open slots'
                vetoed.append(cand)
                continue

            # Gate 2c: Correlation cluster firewall
            if cand.cluster and cand.cluster in used_clusters:
                cand.admitted = False
                cand.veto_reason = f'Cluster veto: {cand.cluster}'
                vetoed.append(cand)
                continue

            # Gate 2d: Negative EV block
            if cand.ev_score <= 0:
                cand.admitted = False
                cand.veto_reason = f'Negative EV ({cand.ev_score:.3f})'
                vetoed.append(cand)
                continue

            # Admitted!
            cand.admitted = True
            if cand.cluster:
                used_clusters.add(cand.cluster)
            admitted.append(cand)
            log.info(
                f'AUCTION ADMIT: {cand.symbol} {cand.direction} | '
                f'P={cand.prob_win:.3f} EV={cand.ev_score:.3f} Score={cand.composite_score:.2f} '
                f'Calmar={self.pool.get_calmar(cand.symbol):.1f}'
            )

        if vetoed:
            for v in vetoed:
                log.debug(f'VETO: {v.symbol} -- {v.veto_reason}')

        return AuctionResult(
            admitted=admitted, vetoed=vetoed, bar_time=bar_time,
            open_slots=open_slots, pool_size=len(self.pool)
        )

    def summary(self, result: AuctionResult) -> str:
        lines = [
            f'[{result.bar_time:%H:%M UTC}] Auction: {len(result.admitted)} admitted, '
            f'{len(result.vetoed)} vetoed | Pool={result.pool_size} | Slots={result.open_slots}'
        ]
        for s in result.admitted:
            lines.append(
                f'  + {s.symbol:<12s} {s.direction:<4s} P={s.prob_win:.3f} '
                f'Score={s.composite_score:.2f} Calmar={self.pool.get_calmar(s.symbol):.1f}'
            )
        return '\n'.join(lines)


# ─── QUICK SELF-TEST ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    from datetime import datetime, timezone
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    engine = AuctionEngine(max_slots=3)
    now = datetime.now(timezone.utc)

    # Simulate a bar where 5 assets fire signals simultaneously
    test_candidates = [
        SignalCandidate('EURUSD',  'BUY',  0.61, 0.05, 0.0008, now),
        SignalCandidate('GAS',     'BUY',  0.58, 0.07, 0.002,  now),
        SignalCandidate('US2000',  'SELL', 0.57, 0.04, 0.50,   now),
        SignalCandidate('AUDCHF',  'BUY',  0.56, 0.06, 0.0005, now),
        SignalCandidate('NICKEL',  'BUY',  0.55, 0.09, 0.015,  now),
        SignalCandidate('GBPUSD',  'BUY',  0.60, 0.04, 0.0007, now),  # USD_BLOC
        SignalCandidate('UNKNOWN', 'BUY',  0.70, 0.01, 0.001,  now),  # not in pool
    ]

    result = engine.rank_signals(test_candidates, open_symbols={'GER40'})
    print(engine.summary(result))
    print(f'\nAdmitted: {[s.symbol for s in result.admitted]}')
    print(f'Vetoed:   {[(s.symbol, s.veto_reason) for s in result.vetoed]}')
