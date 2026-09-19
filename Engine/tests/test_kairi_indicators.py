"""
Unit Tests for Canonical Kairi Relative Index (KRI) and Kairi ATR Ratio
Asserts prefix invariance, causality, and mathematical exactness.
"""
import numpy as np
import pytest
from Engine.core.canonical_indicators import (
    compute_kairi_relative_index,
    compute_kairi_atr_ratio,
    compute_sma_series,
)

def test_kairi_mathematical_definition():
    closes = np.array([100.0, 102.0, 104.0, 106.0, 108.0], dtype=np.float64)
    period = 3
    kri = compute_kairi_relative_index(closes, period=period)
    sma = compute_sma_series(closes, period)

    expected = (closes - sma) / sma * 100.0
    np.testing.assert_allclose(kri, expected, rtol=1e-7, atol=1e-7)

def test_kairi_prefix_invariance():
    rng = np.random.default_rng(42)
    closes = 100.0 + np.cumsum(rng.normal(0, 1, 500))
    period = 20

    full_kri = compute_kairi_relative_index(closes, period=period)
    prefix_kri = compute_kairi_relative_index(closes[:250], period=period)

    np.testing.assert_allclose(full_kri[:250], prefix_kri, rtol=1e-12, atol=1e-12)

def test_kairi_atr_ratio():
    closes = np.array([100.0, 105.0, 110.0], dtype=np.float64)
    atrs = np.array([2.0, 2.5, 3.0], dtype=np.float64)
    period = 2
    kri_atr = compute_kairi_atr_ratio(closes, atrs, period=period)
    sma = compute_sma_series(closes, period)

    expected = (closes - sma) / atrs
    np.testing.assert_allclose(kri_atr, expected, rtol=1e-7, atol=1e-7)

def test_kairi_edge_cases():
    empty = np.array([], dtype=np.float64)
    assert len(compute_kairi_relative_index(empty)) == 0
    assert len(compute_kairi_atr_ratio(empty, empty)) == 0

    zeros = np.zeros(10, dtype=np.float64)
    res = compute_kairi_relative_index(zeros)
    assert np.all(np.isfinite(res))
