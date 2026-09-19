"""Offline contract regressions for the Trading execution path.
Usage: python Engine/tests/test_execution_safety.py --repo . -v
Reads reviewed Python sources, extracts selected definitions with AST, and uses
only fake broker objects. No repository imports, credentials or MT5 connections.
Source extraction is not a security sandbox: review future source changes first.
These desired-safety tests were authored during the Ox_Alpha_40 audit.
"""
import argparse
import ast
import json
import logging
from pathlib import Path
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import Mock
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

REPO = Path(__file__).resolve().parents[2]

def selected_definitions(path, names, namespace, method_names=None):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    selected = []
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in names:
            if isinstance(node, ast.ClassDef) and method_names is not None:
                node.body = [n for n in node.body if isinstance(n, ast.FunctionDef) and n.name in method_names]
            selected.append(node)
    found = {n.name for n in selected}
    if found != set(names):
        raise ValueError(f'{path}: missing definitions {set(names)-found}')
    isolated = ast.fix_missing_locations(ast.Module(body=selected, type_ignores=[]))
    exec(compile(isolated, str(path), 'exec'), namespace)
    return namespace

class SafetyContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='ox40-safety-')
        cls.ns = dict(Path=Path, logging=logging, json=json, time=time,
                      STATE_FILE=Path(cls.temp.name)/'nonexistent_state.json',
                      MAX_CONCURRENT_POSITIONS=3, MAX_MARGIN_UTILIZATION_PCT=.30,
                      MIN_MARGIN_LEVEL_PCT=200.)
        selected_definitions(REPO/'Engine/live/order_manager.py', {'OrderManager'}, cls.ns,
                             {'load_state','reconcile_with_broker','calculate_lot_size','modify_sl'})
        # Evaluate only the literal cluster map, not any top-level executable code.
        auction_path = REPO/'Engine/research/signal_auction.py'
        tree = ast.parse(auction_path.read_text(encoding='utf-8-sig'))
        cluster_node = next(n for n in tree.body if isinstance(n,ast.AnnAssign)
                            and isinstance(n.target,ast.Name) and n.target.id=='CORRELATION_CLUSTERS')
        module = types.ModuleType('_ox40_isolated_auction')
        sys.modules[module.__name__] = module
        cls.au = module.__dict__
        cls.au.update(dict(dataclass=dataclass,field=field,asdict=asdict,Dict=Dict,List=List,
                           Optional=Optional,Set=Set,datetime=datetime,timezone=timezone,
                           CORRELATION_CLUSTERS=ast.literal_eval(cluster_node.value),
                           WIN_R=2.5,LOSS_R=1.0,APPROVED_POOL_PATH='unused',
                           log=logging.getLogger('isolated-auction')))
        selected_definitions(auction_path, {'SignalCandidate','AuctionResult','AuctionEngine','_get_cluster'},cls.au)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
        sys.modules.pop('_ox40_isolated_auction',None)

    def setUp(self):
        self.broker = types.SimpleNamespace(
            positions_get=Mock(return_value=[]), symbol_info=Mock(return_value=None),
            account_info=Mock(return_value=types.SimpleNamespace(equity=5000.,leverage=30.)),
            order_calc_margin=Mock(return_value=1000.),order_send=Mock(return_value=None),
            ORDER_TYPE_BUY=0,POSITION_TYPE_BUY=0,TRADE_ACTION_SLTP=6,TRADE_RETCODE_DONE=10009)
        self.ns['mt5'] = self.broker
        self.manager = self.ns['OrderManager']()
        self.manager.conn = types.SimpleNamespace(
            connected=True,resolve_symbol=lambda s:s,
            get_last_tick=lambda s:types.SimpleNamespace(bid=1.1,ask=1.10002))
        self.manager.open_trades={1:{'symbol':'EURUSD','sl':1.09}}
        self.manager.save_state=Mock()

    def test_query_failure_preserves_positions(self):
        self.broker.positions_get.return_value=None
        self.manager.reconcile_with_broker()
        self.assertIn(1,self.manager.open_trades,'Unknown broker state must not be recorded as closure')

    def test_missing_state_still_discovers_broker_positions(self):
        self.manager.load_state()
        self.broker.positions_get.assert_called()

    def test_missing_symbol_specs_abstains(self):
        self.assertEqual(self.manager.calculate_lot_size('EURUSD',1.,.01),0.)

    def test_minimum_lot_cannot_override_risk_budget(self):
        self.broker.symbol_info.return_value=types.SimpleNamespace(
            trade_tick_value=1.,trade_tick_size=.00001,point=.00001,
            trade_contract_size=100000.,volume_step=.01,volume_min=.01,volume_max=10.)
        lots=self.manager.calculate_lot_size('EURUSD',risk_usd=1.,sl_dist=.01)
        self.assertLessEqual(lots*1000.,1.,'Below-minimum affordable volume must mean no trade')

    def test_none_modify_result_fails_without_exception(self):
        self.broker.positions_get.return_value=[types.SimpleNamespace(symbol='EURUSD',type=0,tp=1.12)]
        try:
            result=self.manager.modify_sl(1,1.095)
        except Exception as exc:
            self.fail(f'Uncaught {type(exc).__name__}: {exc}')
        self.assertIs(result,False)

    def auction(self):
        a=self.au['AuctionEngine'].__new__(self.au['AuctionEngine'])
        a.max_slots=3
        a.pool=types.SimpleNamespace(is_approved=lambda s:True,get_calmar=lambda s:20.)
        # rank_signals calls len(pool); use a tiny explicit fake instead.
        class Pool:
            def is_approved(self,s):return True
            def get_calmar(self,s):return 20.
            def __len__(self):return 18
        a.pool=Pool()
        return a

    def candidate(self,s):
        return self.au['SignalCandidate'](s,'BUY',.6,.05,.001,datetime(2026,9,18,tzinfo=timezone.utc))

    def test_existing_cluster_is_reserved(self):
        result=self.auction().rank_signals([self.candidate('EURSEK')],{'EURUSD'})
        self.assertEqual(len(result.admitted),0,'Existing EURUSD must reserve EUR_BLOC')

    def test_duplicate_symbol_is_rejected(self):
        result=self.auction().rank_signals([self.candidate('EURUSD')],{'EURUSD'})
        self.assertEqual(len(result.admitted),0)

    def test_slot_cap_counts_existing_positions(self):
        result=self.auction().rank_signals([self.candidate('GAS'),self.candidate('NZDCNH')],{'EURUSD','GER40'})
        self.assertLessEqual(len(result.admitted),1)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',default='.',type=Path)
    args,remaining=ap.parse_known_args()
    REPO=args.repo.resolve()
    for f in ('Engine/live/order_manager.py','Engine/research/signal_auction.py'):
        if not (REPO/f).is_file():ap.error(f'Missing {f}')
    unittest.main(argv=[sys.argv[0]]+remaining)
