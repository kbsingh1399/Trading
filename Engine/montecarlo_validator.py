'''
MONTECARLO_VALIDATOR.PY
Institutional 1,000-Path Monte Carlo Bootstrap Stress Tester
Computes VaR, CVaR (Expected Shortfall), Drawdown Distributions, and Confidence Intervals.
'''

import numpy as np

def run_monte_carlo_bootstrap(trade_pnls, initial_capital=5000.0, n_paths=1000, seed=42):
    '''
    trade_pnls: 1D numpy array of net dollar PnL per trade (after 41 bps friction).
    '''
    np.random.seed(seed)
    n_trades = len(trade_pnls)
    if n_trades == 0:
        return {}
        
    final_equities = np.zeros(n_paths)
    max_drawdowns = np.zeros(n_paths)
    
    for p in range(n_paths):
        sampled_pnls = np.random.choice(trade_pnls, size=n_trades, replace=True)
        equity_curve = initial_capital + np.cumsum(sampled_pnls)
        equity_curve = np.insert(equity_curve, 0, initial_capital)
        
        final_equities[p] = equity_curve[-1]
        
        peaks = np.maximum.accumulate(equity_curve)
        dds = (peaks - equity_curve) / peaks
        max_drawdowns[p] = np.max(dds)
        
    roi_distribution = ((final_equities - initial_capital) / initial_capital) * 100.0
    dd_distribution = max_drawdowns * 100.0
    
    mean_roi = np.mean(roi_distribution)
    median_roi = np.median(roi_distribution)
    ci_5 = np.percentile(roi_distribution, 5.0)
    ci_95 = np.percentile(roi_distribution, 95.0)
    
    max_dd_95 = np.percentile(dd_distribution, 95.0)
    max_dd_99 = np.percentile(dd_distribution, 99.0)
    
    trades_per_q = max(1, n_trades // 20)
    quarterly_returns = []
    for p in range(n_paths):
        sampled_pnls = np.random.choice(trade_pnls, size=trades_per_q, replace=True)
        q_ret = (np.sum(sampled_pnls) / initial_capital) * 100.0
        quarterly_returns.append(q_ret)
        
    quarterly_returns = np.array(quarterly_returns)
    var_95 = np.percentile(quarterly_returns, 5.0)
    cvar_95 = np.mean(quarterly_returns[quarterly_returns <= var_95])
    
    prob_ruin_10dd = np.mean(dd_distribution > 10.0) * 100.0
    
    return {
        'n_paths': n_paths,
        'n_trades': n_trades,
        'mean_roi_pct': mean_roi,
        'median_roi_pct': median_roi,
        'ci_95_range_pct': (ci_5, ci_95),
        'max_dd_95th_pct': max_dd_95,
        'max_dd_99th_pct': max_dd_99,
        'quarterly_var_95_pct': var_95,
        'quarterly_cvar_95_pct': cvar_95,
        'prob_drawdown_gt_10pct': prob_ruin_10dd
    }

if __name__ == '__main__':
    synthetic_trades = np.random.normal(loc=11.85, scale=45.0, size=756)
    res = run_monte_carlo_bootstrap(synthetic_trades)
    print('Monte Carlo 1,000-Path Summary:')
    for k, v in res.items():
        print(f'  {k}: {v}')
