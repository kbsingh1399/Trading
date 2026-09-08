"""Causal execution, label alignment and purged training regression checks."""
import numpy as np
import pandas as pd
import pytest

from Engine.core.execution_kernel import ExecutionKernel, FrictionConfig, RatchetConfig
from Engine.core.institutional_meta_labeler import InstitutionalMetaLabeler
from Engine.optimize_individual_assets import STRATEGIES, passes_criteria


def bars(n=32):
    return pd.DataFrame({
        "datetime_utc": pd.date_range("2020-01-01", periods=n, freq="15min", tz="UTC"),
        "open": 100., "high": 100.1, "low": 99.9, "close": 100.,
        "volume_base": 100., "atr_14": 1., "future_cvd_15m": -5.,
        "spot_cvd_15m": 5., "zc_div": 10., "long_liq_zs": 2.,
        "short_liq_zs": 0., "rsi_14": 30., "vwap_zscore": -1., "ema_200": 100.,
    })


def signals(df, positions=(0,), side=1):
    result = pd.DataFrame({"side": np.zeros(len(df), dtype=int), "raw_r": 0.}, index=df.index)
    result.iloc[list(positions), :] = [side, 1.]
    return result


def frictionless():
    return ExecutionKernel(fric_cfg=FrictionConfig(0., 0., 0.))


@pytest.mark.parametrize("side", [1, -1])
def test_entry_bar_stop_first_and_no_retroactive_reentry(side):
    df = bars(4)
    df.loc[1, ["high", "low"]] = [104., 96.]
    result = frictionless().run(df, signals(df, (0,), side))
    assert result["trades"] == 1
    trade = result["trades_list"][0]
    assert trade["entry_bar"] == trade["exit_bar"] == 1
    assert trade["reason"] == "STOP_BAR"
    assert trade["pnl"] == pytest.approx(-25.)


def test_no_reentry_after_intrabar_exit():
    df = bars(5)
    df.loc[2, "low"] = 98.
    result = frictionless().run(df, signals(df, (0, 1)))
    assert result["trades"] == 1
    assert result["trades_list"][0]["exit_bar"] == 2


def test_entry_bar_target():
    df = bars(4)
    df.loc[1, "high"] = 104.
    trade = frictionless().run(df, signals(df))["trades_list"][0]
    assert trade["exit_bar"] == 1
    assert trade["exit"] == pytest.approx(102.5)


def test_target_gap_does_not_credit_profit_above_target_or_phantom_peak():
    df = bars(4)
    df.loc[2, ["open", "high", "low", "close"]] = [120., 121., 119., 120.]
    result = frictionless().run(df, signals(df))
    assert result["trades_list"][0]["exit"] == pytest.approx(102.5)
    assert result["max_dd_pct"] < 1.


def test_gap_loss_is_not_clipped_and_halts_new_entries():
    df = bars(6)
    df.loc[2, ["open", "high", "low", "close"]] = [80., 81., 79., 80.]
    result = frictionless().run(df, signals(df, (0, 2, 3)))
    assert result["trades"] == 1
    assert result["max_dd_pct"] >= 10.
    assert result["halted"]


def test_ratchet_becomes_effective_next_bar():
    df = bars(4)
    df.loc[1, ["high", "low", "close"]] = [101., 99.5, 100.9]
    df.loc[2, ["open", "high", "low", "close"]] = [100.9, 101., 100., 100.3]
    trade = frictionless().run(df, signals(df))["trades_list"][0]
    assert trade["exit_bar"] == 2
    assert trade["exit"] == pytest.approx(100.15)


def test_decay_counts_entry_bar_and_uses_current_gain():
    df = bars(30)
    # Earlier +0.3R does not exempt a subsequently stagnant trade.
    df.loc[2, "high"] = 100.3
    trade = frictionless().run(df, signals(df))["trades_list"][0]
    assert trade["exit_bar"] == 24
    assert trade["reason"] == "TIME_DECAY"


def test_decay_is_conditional_not_hard_24_bar_horizon():
    df = bars(30)
    df.loc[1:, ["high", "close"]] = [100.4, 100.3]
    df.loc[25, "high"] = 103.
    trade = frictionless().simulate_event(df, 0, 1, 1.)
    assert trade["exit_bar"] == 25
    assert trade["reason"] == "TARGET_BAR"


def test_friction_sizing_and_terminal_settlement():
    df = bars(5)
    df.loc[1, "low"] = 98.
    trade = ExecutionKernel().run(df, signals(df))["trades_list"][0]
    assert trade["pnl"] == pytest.approx(-25.)
    terminal = ExecutionKernel().run(bars(5), signals(bars(5)))["trades_list"][0]
    assert terminal["reason"] == "TERMINAL_SETTLEMENT"
    assert terminal["pnl"] < 0


def test_features_prefix_and_short_orientation():
    df = bars(100)
    full = InstitutionalMetaLabeler.extract_features(df)
    pd.testing.assert_frame_equal(full.iloc[:60], InstitutionalMetaLabeler.extract_features(df.iloc[:60]))
    x = InstitutionalMetaLabeler.event_features(df, signals(df, (30,), -1))
    assert x.loc[30, "zc_div"] == pytest.approx(-0.1)
    assert x.loc[30, "rsi_14"] == pytest.approx(0.7)
    assert x.loc[30, "short_liq_zs"] == 2.


def test_event_labels_match_kernel_and_drop_censoring():
    df = bars(35)
    df.loc[25, "high"] = 103.
    df.loc[28, "low"] = 98.
    primary = signals(df, (24, 27, 32))
    labeler = InstitutionalMetaLabeler(frictionless())
    events = labeler.label_events(df, primary)
    assert events.bar.tolist() == [24, 27]
    assert events.label.tolist() == [1, 0]


def test_actual_training_purge_and_inference_prefix():
    df = bars(6000)
    primary = signals(df, tuple(range(30, 5600, 10)))
    for k, t in enumerate(range(30, 5600, 10)):
        df.loc[t + 1, "high" if k % 2 else "low"] = 103. if k % 2 else 98.
    start = df.datetime_utc.iloc[5900]
    labeler = InstitutionalMetaLabeler(frictionless()).fit(df, primary, start)
    assert pd.Timestamp(labeler.audit["latest_label_end"]) < start - pd.Timedelta(hours=72)
    assert labeler.audit["folds"]
    for fold in labeler.audit["folds"]:
        assert pd.Timestamp(fold["train_end"]) < pd.Timestamp(fold["validation_start"]) - pd.Timedelta(hours=72)
    candidate = signals(df, (5901, 5920))
    full = labeler.filter_signals(df, candidate)
    prefix = labeler.filter_signals(df.iloc[:5930], candidate.iloc[:5930])
    pd.testing.assert_frame_equal(full.iloc[:5930], prefix)
    with pytest.raises(ValueError, match="precede"):
        labeler.filter_signals(df, signals(df, (30,)))


@pytest.mark.parametrize("strategy_class", STRATEGIES)
def test_strategy_defaults_and_signal_prefix(strategy_class):
    simulator = strategy_class()
    assert simulator.kernel.ratchet == RatchetConfig()
    df = bars(150)
    full = simulator.generate_signals(df)
    prefix = simulator.generate_signals(df.iloc[:100])
    pd.testing.assert_frame_equal(full.iloc[:100], prefix)
    assert simulator.generate_signals(df.iloc[:0]).empty


def test_strict_pass_boundaries():
    criteria = dict(min_roi_percent=20., max_dd_percent=5., min_winrate_percent=40., min_trades=6)
    base = dict(roi_pct=21., max_dd_pct=4., win_rate_pct=41., trades=6)
    assert passes_criteria(base, criteria)
    for key, value in (("roi_pct", 20.), ("max_dd_pct", 5.), ("win_rate_pct", 40.), ("trades", 5)):
        assert not passes_criteria(dict(base, **{key: value}), criteria)
