"""
Lesson 0.2 -- Discrete time & integration
==========================================

The one idea: your simulator doesn't integrate a differential equation --
it multiplies by a fixed ratio every step. Whether that ratio's magnitude
is above or below 1 decides everything, and that ratio depends on `dt`.

Run this file top to bottom (`python lesson.py`). The hook below runs
immediately, no dependencies. The comparison section further down needs
`euler_step`, `rk4_step` and `simulate` filled in inside `srlib/sim.py` --
that's the actual work of this lesson. Until you do that, running past the
hook will raise NotImplementedError, which is expected.
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

import sys
from pathlib import Path

# Same trick as L0.1 -- lesson.py lives two folders below the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from srlib.sim import euler_step, rk4_step, simulate

# Save output next to this script, not wherever the process happened to be
# launched from -- avoids the PNG silently landing outside the lesson folder.
OUTPUT_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Part 1 -- the hook: watch the recurrence e_n = (1 - k*dt)^n * e0 explode
# ---------------------------------------------------------------------------

def hook_euler_instability() -> None:
    """No simulator involved -- just the recurrence you derived by hand in
    notes.md. This is exactly what euler_step does once you implement it,
    applied to Newton's law of cooling."""
    k = 1.5     # cooling rate constant [1/s]
    e0 = 70.0   # initial error from room temperature [deg C]
    threshold = 2.0 / k

    print(f"Stability threshold: dt < 2/k = {threshold:.3f} s\n")

    for dt, label in [(0.1, "well inside the threshold"),
                       (1.6, "past the threshold")]:
        r = 1 - k * dt
        print(f"dt = {dt}  ({label}), r = 1 - k*dt = {r:.3f}")
        e = e0
        for n in range(6):
            print(f"  step {n}: error = {e:9.3f}")
            e *= r
        print()


# ---------------------------------------------------------------------------
# Part 2 -- the system: a cup of coffee cooling to room temperature
# ---------------------------------------------------------------------------

K = 1.5        # cooling rate constant [1/s]
X_ROOM = 20.0  # room temperature [deg C]


def coffee_dynamics(t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
    """dx/dt = -k*(x - x_room) -- Newton's law of cooling. `u` is unused --
    there's no controller here, just physics -- but every Dynamics function
    in this course takes (t, x, u) so `simulate` can treat every lesson the
    same way, controlled or not."""
    return -K * (x - X_ROOM)


def no_controller(t: float, x: np.ndarray) -> np.ndarray:
    return np.zeros_like(x)


def analytic_solution(t: np.ndarray, x0: float) -> np.ndarray:
    """Closed-form solution, for comparison only -- never used inside the
    simulator itself."""
    return X_ROOM + (x0 - X_ROOM) * np.exp(-K * t)


# ---------------------------------------------------------------------------
# Part 3 -- run three simulations and compare
# ---------------------------------------------------------------------------

def run_comparison():
    x0 = np.array([90.0])
    t_end = 15.0
    dt_small = 0.1
    dt_big = 1.6   # > 2/K = 1.333 -- past Euler's stability threshold

    data_euler_small = simulate(coffee_dynamics, x0, no_controller, t_end, dt_small, integrator=euler_step)
    data_euler_big = simulate(coffee_dynamics, x0, no_controller, t_end, dt_big, integrator=euler_step)
    data_rk4_big = simulate(coffee_dynamics, x0, no_controller, t_end, dt_big, integrator=rk4_step)

    return data_euler_small, data_euler_big, data_rk4_big


def plot_comparison(data_euler_small, data_euler_big, data_rk4_big) -> None:
    # Euler at dt=1.6 swings into the thousands, which flattens everything
    # else onto a line near zero if it shares an axis with them. Two panels,
    # same data: the top shows the full blow-up, the bottom only plots the
    # well-behaved series, so matplotlib autoscales it to THEIR range and
    # you can actually see Euler(dt=0.1) vs RK4(dt=1.6) against the analytic
    # curve.
    t_fine = np.linspace(0, 15.0, 300)
    analytic = analytic_solution(t_fine, 90.0)

    fig, (ax_full, ax_zoom) = plt.subplots(2, 1, figsize=(7, 8.5))

    ax_full.plot(t_fine, analytic, "k--", label="analytic solution", linewidth=1.5)
    ax_full.plot(data_euler_small["t"], data_euler_small["x"][:, 0], "o-", label="Euler, dt=0.1 (stable)")
    ax_full.plot(data_euler_big["t"], data_euler_big["x"][:, 0], "o-", label="Euler, dt=1.6 (unstable)")
    ax_full.plot(data_rk4_big["t"], data_rk4_big["x"][:, 0], "s-", label="RK4, dt=1.6 (same dt as unstable Euler)")
    ax_full.axhline(X_ROOM, color="gray", linewidth=0.8)
    ax_full.set_ylabel("temperature [deg C]")
    ax_full.set_title("Full range -- the Euler blow-up dominates the scale", fontsize=10)
    ax_full.legend(fontsize=8)

    ax_zoom.plot(t_fine, analytic, "k--", label="analytic solution", linewidth=1.5)
    ax_zoom.plot(data_euler_small["t"], data_euler_small["x"][:, 0], "o-", label="Euler, dt=0.1 (stable)")
    ax_zoom.plot(data_rk4_big["t"], data_rk4_big["x"][:, 0], "s-", label="RK4, dt=1.6")
    ax_zoom.axhline(X_ROOM, color="gray", linewidth=0.8)
    ax_zoom.set_xlabel("t [s]")
    ax_zoom.set_ylabel("temperature [deg C]")
    ax_zoom.set_title("Zoomed -- unstable Euler left out so the axes autoscale to the rest", fontsize=10)
    ax_zoom.legend(fontsize=8)

    fig.suptitle("L0.2 -- Euler vs RK4, coffee cooling")
    fig.tight_layout()
    out_path = OUTPUT_DIR / "integrators.png"
    fig.savefig(out_path)
    print(f"Saved {out_path} -- open it and compare to your prediction.")


if __name__ == "__main__":
    hook_euler_instability()
    print("Before running the sim: for each of the three lines below, sketch (paper or in")
    print("your head) what you expect to see over 15 seconds:")
    print("  1. Euler, dt=0.1")
    print("  2. Euler, dt=1.6")
    print("  3. RK4,   dt=1.6  <- same dt as #2. What's different is the INTEGRATOR, not dt.")
    print()
    data_euler_small, data_euler_big, data_rk4_big = run_comparison()
    plot_comparison(data_euler_small, data_euler_big, data_rk4_big)
