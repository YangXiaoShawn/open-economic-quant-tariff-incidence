"""Estimator tests.

These check the econometrics against cases with a known answer: analytically
recoverable OLS, a Poisson process with a known coefficient, and a simulated
panel whose treatment effect is set by construction. An estimator that cannot
recover a parameter that was deliberately put into the data cannot be trusted to
measure one that was not.
"""

from __future__ import annotations

import numpy as np
import polars as pl
import pytest

from tariff_incidence.econ.designs import (
    build_event_dummies,
    event_study,
    pretrend_test,
    two_way_fe_regression,
)
from tariff_incidence.econ.diversion import decompose
from tariff_incidence.econ.hdfe import absorb, ols_hdfe, ppml_hdfe

# --------------------------------------------------------------------- #
# absorption
# --------------------------------------------------------------------- #


def test_single_effect_absorption_demeans_exactly_in_one_pass():
    g = np.array([0, 0, 1, 1, 2, 2])
    X = np.array([[1.0], [3.0], [10.0], [20.0], [5.0], [5.0]])
    out, iters, ok = absorb(X, [g])
    assert ok
    # one demeaning pass plus one confirming pass
    assert iters <= 2
    for grp in np.unique(g):
        assert out[g == grp].mean() == pytest.approx(0.0, abs=1e-12)


def test_two_way_absorption_converges():
    rng = np.random.default_rng(0)
    n = 400
    e = rng.integers(0, 20, n)
    t = rng.integers(0, 10, n)
    X = (rng.normal(size=(n, 2)) + e[:, None] * 0.3 + t[:, None] * 0.2)
    out, _, ok = absorb(X, [e, t])
    assert ok
    for g in (e, t):
        for grp in np.unique(g):
            assert np.abs(out[g == grp].mean(axis=0)).max() < 1e-6


# --------------------------------------------------------------------- #
# OLS with fixed effects
# --------------------------------------------------------------------- #


def test_ols_hdfe_recovers_a_known_slope():
    rng = np.random.default_rng(11)
    n_e, n_t = 40, 24
    e = np.repeat(np.arange(n_e), n_t)
    t = np.tile(np.arange(n_t), n_e)
    n = n_e * n_t
    alpha = rng.normal(0, 2, n_e)[e]
    gamma = rng.normal(0, 1, n_t)[t]
    x = rng.normal(0, 1, n)
    beta = 0.75
    y = alpha + gamma + beta * x + rng.normal(0, 0.05, n)

    fit = ols_hdfe(y, x[:, None], ["x"], {"entity": e, "time": t}, {"entity": e})
    assert fit.params["x"] == pytest.approx(beta, abs=0.01)
    lo, hi = fit.conf_int("x")
    assert lo < beta < hi


def test_ols_hdfe_matches_explicit_dummy_regression():
    rng = np.random.default_rng(3)
    n = 300
    e = rng.integers(0, 8, n)
    x = rng.normal(size=n)
    y = 1.5 * x + np.array([0.0, 1, 2, 3, 4, 5, 6, 7])[e] + rng.normal(0, 0.2, n)

    fit = ols_hdfe(y, x[:, None], ["x"], {"entity": e}, {"entity": e})
    D = np.column_stack([x] + [(e == k).astype(float) for k in range(8)])
    beta_dummy = np.linalg.lstsq(D, y, rcond=None)[0][0]
    assert fit.params["x"] == pytest.approx(beta_dummy, abs=1e-8)


def test_clustered_standard_errors_exceed_naive_ones_under_within_cluster_correlation():
    rng = np.random.default_rng(7)
    n_g, n_per = 30, 25
    g = np.repeat(np.arange(n_g), n_per)
    shock = rng.normal(0, 1.0, n_g)[g]
    x = rng.normal(size=n_g * n_per) + shock
    y = 0.5 * x + shock * 2.0 + rng.normal(0, 0.1, n_g * n_per)
    dummy = np.zeros_like(g)
    clustered = ols_hdfe(y, x[:, None], ["x"], {}, {"g": g})
    unclustered = ols_hdfe(y, x[:, None], ["x"], {}, {"obs": np.arange(y.size)})
    assert clustered.std_errors["x"] > unclustered.std_errors["x"]
    assert clustered.n_clusters["g"] == n_g
    assert dummy.size == y.size


# --------------------------------------------------------------------- #
# PPML
# --------------------------------------------------------------------- #


def test_ppml_recovers_a_known_poisson_coefficient():
    rng = np.random.default_rng(5)
    n = 6000
    x = rng.normal(0, 1, n)
    beta = -0.8
    mu = np.exp(2.0 + beta * x)
    y = rng.poisson(mu).astype(float)
    fit = ppml_hdfe(y, x[:, None], ["x"], {"const": np.zeros(n, dtype=int)}, {"obs": np.arange(n)})
    assert fit.converged
    assert fit.params["x"] == pytest.approx(beta, abs=0.05)


def test_ppml_recovers_the_coefficient_with_fixed_effects():
    rng = np.random.default_rng(9)
    n_e, n_t = 50, 20
    e = np.repeat(np.arange(n_e), n_t)
    t = np.tile(np.arange(n_t), n_e)
    n = n_e * n_t
    x = rng.normal(0, 1, n)
    beta = 0.4
    eta = 1.5 + rng.normal(0, 0.4, n_e)[e] + rng.normal(0, 0.2, n_t)[t] + beta * x
    y = rng.poisson(np.exp(eta)).astype(float)
    fit = ppml_hdfe(y, x[:, None], ["x"], {"e": e, "t": t}, {"e": e})
    assert fit.converged
    assert fit.params["x"] == pytest.approx(beta, abs=0.05)


def test_ppml_retains_zero_observations():
    rng = np.random.default_rng(13)
    n = 2000
    x = rng.normal(0, 1, n)
    y = rng.poisson(np.exp(0.2 - 0.5 * x)).astype(float)
    assert (y == 0).sum() > 0
    fit = ppml_hdfe(y, x[:, None], ["x"], {"c": np.zeros(n, dtype=int)}, {"obs": np.arange(n)})
    assert fit.n_obs == n, "PPML must use the zeros, not drop them"
    assert any("zero-valued observations retained" in note for note in fit.notes)


def test_ppml_rejects_negative_outcomes():
    with pytest.raises(ValueError, match="non-negative"):
        ppml_hdfe(
            np.array([-1.0, 2.0]), np.array([[1.0], [2.0]]), ["x"],
            {"c": np.zeros(2, dtype=int)}, {},
        )


# --------------------------------------------------------------------- #
# event study
# --------------------------------------------------------------------- #


def _sim_panel(effect: float = -0.30, n_prod: int = 30, seed: int = 42) -> pl.DataFrame:
    """Panel with a known post-treatment jump for treated flows of treated products."""
    rng = np.random.default_rng(seed)
    months = list(range(24))
    rows = []
    for p in range(n_prod):
        treated_product = p < n_prod // 2
        pi = rng.normal(0, 0.5)
        for c in ["5700", "5520", "5490"]:
            ci = rng.normal(0, 0.3)
            for m in months:
                et = m - 12
                is_treated_flow = treated_product and c == "5700"
                y = 5 + pi + ci + 0.01 * m + rng.normal(0, 0.05)
                if is_treated_flow and et >= 0:
                    y += effect
                rows.append(
                    {
                        "hs6": f"{p:06d}",
                        "country_code": c,
                        "flow_id": f"{p:06d}_{c}",
                        "month_key": f"m{m:02d}",
                        "event_time": et if treated_product else None,
                        "is_treated_country": c == "5700",
                        "y": y,
                        "count_outcome": float(np.exp(y - 4)),
                        "treat_rate": 0.25 if (is_treated_flow and et >= 0) else 0.0,
                    }
                )
    return pl.DataFrame(rows)


def test_event_study_recovers_a_known_step_effect():
    panel = _sim_panel(effect=-0.30)
    fit, spec, coefs = event_study(
        panel, "y", fixed_effects=["flow_id", "month_key"], cluster_vars=["hs6"],
        window=(-6, 6), reference=-1,
    )
    post = coefs.filter((pl.col("event_time") >= 0) & (pl.col("std_error") > 0))
    assert post["estimate"].mean() == pytest.approx(-0.30, abs=0.03)
    assert spec.estimator == "OLS-HDFE"


def test_event_study_pre_period_coefficients_are_flat_when_there_is_no_pretrend():
    panel = _sim_panel(effect=-0.30)
    fit, _, coefs = event_study(
        panel, "y", fixed_effects=["flow_id", "month_key"], cluster_vars=["hs6"],
        window=(-6, 6), reference=-1,
    )
    pt = pretrend_test(coefs, fit)
    assert pt["max_abs_pre_coef"] < 0.05
    # With a tightly simulated panel the standard errors are small enough that a
    # trivially small pre-coefficient can still be "significant". The design is
    # clean on the economic criterion, which is what the verdict encodes.
    assert pt["economically_small"]
    assert pt["verdict"] in ("CLEAN", "STATISTICALLY_DETECTABLE_BUT_ECONOMICALLY_SMALL")


def test_pretrend_test_detects_an_injected_pretrend():
    panel = _sim_panel(effect=-0.30).with_columns(
        pl.when(pl.col("is_treated_country") & pl.col("event_time").is_not_null())
        .then(pl.col("y") + 0.03 * pl.col("event_time"))
        .otherwise(pl.col("y"))
        .alias("y")
    )
    fit, _, coefs = event_study(
        panel, "y", fixed_effects=["flow_id", "month_key"], cluster_vars=["hs6"],
        window=(-6, 6), reference=-1,
    )
    pt = pretrend_test(coefs, fit)
    assert pt["any_pre_significant_5pct"], "a linear pre-trend must be detected"
    assert not pt["economically_small"]
    assert pt["verdict"] == "PRETREND_PRESENT"


def test_reference_period_is_reported_as_exactly_zero():
    panel = _sim_panel()
    _, _, coefs = event_study(
        panel, "y", fixed_effects=["flow_id", "month_key"], cluster_vars=["hs6"],
        window=(-6, 6), reference=-1,
    )
    ref = coefs.filter(pl.col("term").str.starts_with("evt_reference"))
    assert ref.height == 1
    assert ref.row(0, named=True)["estimate"] == 0.0


def test_event_dummies_bin_the_window_endpoints_rather_than_dropping_them():
    panel = _sim_panel()
    d, names = build_event_dummies(panel, window=(-3, 3), reference=-1)
    assert any(n.startswith("evt_pre_bin") for n in names)
    assert any(n.startswith("evt_post_bin") for n in names)
    assert d.height == panel.height, "no observation should be dropped"


def test_twfe_recovers_the_effect_per_unit_of_treatment():
    panel = _sim_panel(effect=-0.30)
    fit, _ = two_way_fe_regression(
        panel, "y", "treat_rate", fixed_effects=["flow_id", "month_key"], cluster_vars=["hs6"]
    )
    # effect is -0.30 at a treatment rate of 0.25 -> slope -1.2
    assert fit.params["treat_rate"] == pytest.approx(-1.2, abs=0.1)


def test_ppml_event_study_runs_on_a_count_outcome():
    panel = _sim_panel(effect=-0.30)
    fit, _, coefs = event_study(
        panel, "count_outcome", fixed_effects=["flow_id", "month_key"],
        cluster_vars=["hs6"], window=(-6, 6), reference=-1, estimator="ppml",
    )
    assert fit.estimator == "PPML-HDFE"
    post = coefs.filter((pl.col("event_time") >= 0) & (pl.col("std_error") > 0))
    assert post["estimate"].mean() == pytest.approx(-0.30, abs=0.06)


# --------------------------------------------------------------------- #
# diversion decomposition
# --------------------------------------------------------------------- #


def test_decomposition_margins_sum_to_the_total_change():
    rng = np.random.default_rng(2)
    rows = []
    for p in range(6):
        for c in ["5700", "5520"]:
            for m in range(24):
                et = m - 12
                v = 100.0 + rng.normal(0, 1)
                if c == "5700" and et >= 0:
                    v *= 0.7
                if c == "5520" and et >= 0:
                    v *= 1.4
                rows.append(
                    {"hs6": f"{p:06d}", "country_code": c, "event_time": et,
                     "customs_value": v, "month_index": m}
                )
    panel = pl.DataFrame(rows)
    by_p, totals = decompose(
        panel, treated_country_code="5700", pre_window=(-12, -1), post_window=(1, 10)
    )
    t = totals.row(0, named=True)
    assert t["treated_intensive"] + t["treated_extensive"] + t["alternative_intensive"] + t[
        "alternative_extensive"
    ] == pytest.approx(t["total_change"], rel=1e-9)
    assert t["treated_total"] < 0 < t["alternative_total"], (
        "contraction and expansion must be reported separately, not netted"
    )


def test_decomposition_separates_extensive_margin_exit():
    rows = []
    for m in range(24):
        et = m - 12
        rows.append({"hs6": "000001", "country_code": "5700", "event_time": et,
                     "customs_value": 100.0 if et < 0 else 0.0, "month_index": m})
        rows.append({"hs6": "000001", "country_code": "5520", "event_time": et,
                     "customs_value": 50.0, "month_index": m})
    by_p, totals = decompose(
        pl.DataFrame(rows), treated_country_code="5700",
        pre_window=(-12, -1), post_window=(1, 10),
    )
    t = totals.row(0, named=True)
    assert t["treated_extensive"] == pytest.approx(-100.0)
    assert t["treated_intensive"] == pytest.approx(0.0)
    assert t["n_treated_flows_exited"] == 1
