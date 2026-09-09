"""
Tests for Lesson 0.2 -- Discrete time & integration.

Run from the repo root:  pytest level0/L0.2_discrete_time_integration/ -v

These check real numerical and stability properties of your euler_step,
rk4_step and simulate implementations in srlib/sim.py -- not string
matches, not bit-exact comparisons against a hidden reference trace.
"""
import numpy as np
import pytest

from srlib.sim import euler_step, rk4_step, simulate
from lesson import coffee_dynamics, no_controller, analytic_solution, K, X_ROOM


def constant_dynamics(t, x, u):
    """A derivative that never changes -- no curvature for either integrator
    to miss."""
    return np.array([2.0, -3.0])


def test_euler_step_exact_for_constant_derivative():
    # If dx/dt never changes, Euler's forward-difference approximation isn't
    # approximating anything -- x(t+dt) = x(t) + dt*f is exact.
    x0 = np.array([1.0, 1.0])
    dt = 0.37
    result = euler_step(constant_dynamics, 0.0, x0, np.zeros(2), dt)
    expected = x0 + dt * np.array([2.0, -3.0])
    np.testing.assert_allclose(result, expected)


def test_rk4_step_exact_for_constant_derivative():
    # k1 == k2 == k3 == k4 when the slope never changes, so RK4 must agree
    # with Euler exactly here. If this fails but the Euler test passes, your
    # rk4_step is evaluating f at the wrong (t, x) for one of the stages.
    x0 = np.array([1.0, 1.0])
    dt = 0.37
    result = rk4_step(constant_dynamics, 0.0, x0, np.zeros(2), dt)
    expected = x0 + dt * np.array([2.0, -3.0])
    np.testing.assert_allclose(result, expected)


def test_rk4_more_accurate_than_euler_for_same_dt():
    x0 = np.array([90.0])
    dt = 0.5
    analytic = analytic_solution(np.array([dt]), 90.0)[0]

    x_euler = euler_step(coffee_dynamics, 0.0, x0, np.zeros(1), dt)
    x_rk4 = rk4_step(coffee_dynamics, 0.0, x0, np.zeros(1), dt)

    euler_err = abs(x_euler[0] - analytic)
    rk4_err = abs(x_rk4[0] - analytic)

    assert rk4_err < 0.5, f"RK4 should be tightly accurate at dt={dt}, got error {rk4_err}"
    assert euler_err > 10 * rk4_err, "RK4 should be far more accurate than Euler at the same dt"


def test_euler_unstable_above_stability_threshold():
    # Threshold is dt < 2/K for this linear decay system; dt=1.6 is past it
    # (2/K = 1.333).
    x0 = np.array([90.0])
    data = simulate(coffee_dynamics, x0, no_controller, t_end=15.0, dt=1.6, integrator=euler_step)
    initial_error = abs(x0[0] - X_ROOM)
    final_error = abs(data["x"][-1, 0] - X_ROOM)
    assert final_error > initial_error, (
        "Euler at dt=1.6 (past the 2/K stability threshold) should diverge, "
        "not settle -- check your euler_step formula."
    )


def test_rk4_stable_at_same_dt_where_euler_diverges():
    x0 = np.array([90.0])
    data = simulate(coffee_dynamics, x0, no_controller, t_end=15.0, dt=1.6, integrator=rk4_step)
    initial_error = abs(x0[0] - X_ROOM)
    final_error = abs(data["x"][-1, 0] - X_ROOM)
    assert final_error < initial_error, (
        "RK4 has a bigger stability region than Euler -- at dt=1.6 it should "
        "still be converging toward room temperature, not diverging."
    )


def test_euler_stable_well_below_threshold():
    x0 = np.array([90.0])
    data = simulate(coffee_dynamics, x0, no_controller, t_end=15.0, dt=0.1, integrator=euler_step)
    final_error = abs(data["x"][-1, 0] - X_ROOM)
    assert final_error < 0.1, "Euler at dt=0.1 should have settled close to room temperature by t=15s"


def test_simulate_logs_expected_time_spacing_and_length():
    x0 = np.array([90.0])
    data = simulate(coffee_dynamics, x0, no_controller, t_end=15.0, dt=1.6, integrator=euler_step)
    t = data["t"]
    assert len(t) == 10, f"expected 10 logged steps for t_end=15, dt=1.6, got {len(t)}"
    np.testing.assert_allclose(np.diff(t), 1.6, atol=1e-9)
    assert t[0] == 0.0, "the first logged entry should be x0 at t=0, logged BEFORE the first step"


def test_simulate_all_signals_same_length():
    x0 = np.array([90.0])
    data = simulate(coffee_dynamics, x0, no_controller, t_end=5.0, dt=0.2, integrator=rk4_step)
    lengths = {key: len(val) for key, val in data.items()}
    assert len(set(lengths.values())) == 1, f"logged signals have mismatched lengths: {lengths}"
