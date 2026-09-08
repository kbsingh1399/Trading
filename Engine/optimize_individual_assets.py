"""Per-asset purged meta-labeling; stop at the first failed window."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import pandas as pd
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent))
from Engine.core.institutional_meta_labeler import InstitutionalMetaLabeler
from Engine.strategy.s1_liquidation_cascade import LiquidationCascadeSimulator
from Engine.strategy.s2_institutional_ml import S2InstitutionalMLSimulator
from Engine.strategy.smc_edgeful import SMCEdgefulSimulator
from Engine.strategy.smc_kane import SMCKaneSimulator
from Engine.strategy.smc_marci import SMCMarciSimulator
from Engine.strategy.smc_marco import SMCMarcoSimulator
from Engine.strategy.smc_mayne import SMCMayneSimulator
from Engine.strategy.smc_usman_noah import SMCUsmanNoahSimulator
STRATEGIES = (LiquidationCascadeSimulator, S2InstitutionalMLSimulator,
              SMCEdgefulSimulator, SMCKaneSimulator, SMCMarciSimulator,
              SMCMarcoSimulator, SMCMayneSimulator, SMCUsmanNoahSimulator)
ASSETS = ('BTC','ETH','XRP','SOL','BNB','DOGE','ADA','TRX','LINK','AVAX',
          'SUI','NEAR','DOT','LTC','BCH','APT','OP','ARB')


def passes_criteria(result, criteria):
    return bool(result['roi_pct'] > criteria['min_roi_percent']
                and result['max_dd_pct'] < criteria['max_dd_percent']
                and result['win_rate_pct'] > criteria['min_winrate_percent']
                and result['trades'] >= criteria['min_trades'])


def evaluate_window(simulator, history, start, end):
    times = InstitutionalMetaLabeler.bar_times(history)
    prefix = history.loc[times < end].copy()
    times = times[times < end]
    expected = pd.date_range(start, end, freq='15min', inclusive='left')
    observed = times[(times >= start) & (times < end)]
    if not observed.equals(expected):
        raise ValueError('OOS coverage incomplete: missing or pre-listing bars')
    candidates = simulator.generate_signals(prefix)
    before = times < start
    labeler = InstitutionalMetaLabeler(kernel=simulator.kernel)
    labeler.fit(prefix.loc[before], candidates.loc[before], oos_start=start)
    inference = candidates.copy()
    inference.loc[before, ['side', 'raw_r']] = 0
    filtered = labeler.filter_signals(prefix, inference)
    result = simulator.kernel.run(prefix.loc[~before], filtered.loc[~before])
    result['meta_audit'] = labeler.audit
    result['primary_candidates'] = int(candidates.loc[~before, 'side'].ne(0).sum())
    result['accepted_candidates'] = int(filtered.loc[~before, 'side'].ne(0).sum())
    return result


def run_optimization(asset):
    asset = asset.upper().removesuffix('USDT')
    if asset not in ASSETS:
        raise ValueError('Asset outside configured universe')
    windows = json.loads((BASE_DIR / 'oos_windows_20.json').read_text())
    criteria = json.loads((BASE_DIR / 'target_oos_criteria.json').read_text())['target_criteria']
    if len(windows) != 20 or criteria['min_r_multiple'] != 2.5:
        raise ValueError('Expected twenty windows and fixed 2.5R target')
    prior_end = None
    for w in windows:
        start = pd.Timestamp(w['start_date'], tz='UTC')
        end = pd.Timestamp(w['end_date'], tz='UTC') + pd.Timedelta(days=1)
        if end <= start or (prior_end is not None and start < prior_end):
            raise ValueError('Windows must be chronological and non-overlapping')
        prior_end = end
    path = BASE_DIR / 'binance_backtesting_data' / f'{asset}USDT_15m_master_2020_2026.parquet'
    frame = pd.read_parquet(path)
    InstitutionalMetaLabeler.bar_times(frame)
    with path.open('rb') as stream:
        fingerprint = hashlib.file_digest(stream, 'sha256').hexdigest()
    sources = [Path(__file__), BASE_DIR / 'core' / 'execution_kernel.py',
               BASE_DIR / 'core' / 'institutional_meta_labeler.py']
    sources += sorted((BASE_DIR / 'strategy').glob('*.py'))
    report = {'asset': asset, 'data_sha256': fingerprint, 'criteria': criteria,
              'data_provenance_certified': False, 'strategies': {},
              'source_sha256': {str(p.relative_to(BASE_DIR)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    for cls in STRATEGIES:
        rows = []
        for w in windows:
            start = pd.Timestamp(w['start_date'], tz='UTC')
            end = pd.Timestamp(w['end_date'], tz='UTC') + pd.Timedelta(days=1)
            try:
                result = evaluate_window(cls(), frame, start, end)
                passed = passes_criteria(result, criteria)
                row = {k: v for k, v in result.items() if k != 'equity_curve'}
                row.update(window=w['name'], passed=passed, status='PASS' if passed else 'FAIL')
            except ValueError as error:
                row = {'window': w['name'], 'passed': False, 'status': 'NOT_EVALUABLE', 'reason': str(error)}
            rows.append(row)
            print(f"{asset} {cls.__name__} {w['name']}: {row['status']}", flush=True)
            if not row['passed']:
                break
        report['strategies'][cls.__name__] = {'passes': sum(r['passed'] for r in rows),
            'required_windows': 20, 'all_pass': len(rows) == 20 and all(r['passed'] for r in rows), 'windows': rows}
    out = BASE_DIR.parent / 'docs' / 'reviews' / 'meta_labeling'
    out.mkdir(parents=True, exist_ok=True)
    (out / f'{asset}_walk_forward.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--asset', choices=ASSETS)
    group.add_argument('--all-assets', action='store_true')
    args = parser.parse_args()
    for ticker in ASSETS if args.all_assets else [args.asset]:
        run_optimization(ticker)
