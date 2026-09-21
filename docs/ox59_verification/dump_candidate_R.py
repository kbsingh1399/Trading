import sys, numpy as np
sys.path.insert(0, sys.argv[1])
from Engine.core.fast_numba_oos_engine import compile_dataset_with_numba
from Engine.strategy.s1_liquidation_orderflow.s1_dual_model_orderflow import InstitutionalDualModelEngine
from Engine.runners.run_20_oos_multiverse import load_cross_asset_orb_crt_pool
pool = compile_dataset_with_numba()
r = pool['realized_r'].to_numpy(float)
print('S1 pool: n=%d meanR=%.4f P(win)=%.3f P(dust 0<r<=.05)=%.3f P(stop<=-1.3)=%.3f P(big>=1)=%.3f' % (
    len(r), r.mean(), (r>0).mean(), ((r>0)&(r<=0.05)).mean(), (r<=-1.3).mean(), (r>=1.0).mean()))
eng = InstitutionalDualModelEngine()
t1 = eng.load_t1_breakout_trades()
tr = t1['r_gain'].to_numpy(float)
print('T1 pool: n=%d meanR=%.4f P(win)=%.3f' % (len(tr), tr.mean(), (tr>0).mean()))
orb = load_cross_asset_orb_crt_pool(crypto_only=True)
o = orb['outcome'].to_numpy(float)
print('ORB pool: n=%d meanR=%.4f P(win)=%.3f' % (len(o), o.mean(), (o>0).mean()))
