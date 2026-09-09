"""Lesson 0.2 -- worked solution. See
level0/L0.2_discrete_time_integration/lesson.py for the exercise version
with commentary, and srlib_sim_integrators.py for the srlib/sim.py pieces
this depends on."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = Path(__file__).resolve().parent

K = 1.5
X_ROOM = 20.0


def euler_step(f, t, x, u, dt):
    k1 = f(t, x, u)
    return x + dt * k1


def rk4_step(f, t, x, u, dt):
    k1 = f(t, x, u)
    k2 = f(t + dt / 2, x + dt / 2 * k1, u)
    k3 = f(t + dt / 2, x + dt / 2 * k2, u)
    k4 = f(t + dt, x + dt * k3, u)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


class Logger:
    def __init__(self):
        self.data = {}

    def record(self, **kwargs):
        for key, value in kwargs.items():
            self.data.setdefault(key, []).append(value)

    def as_dict(self):
        return {key: np.array(values) for key, values in self.data.items()}


def simulate(f, x0, controller, t_end, dt, integrator=rk4_step):
    log = Logger()
    x = x0.copy()
    t = 0.0
    while t < t_end:
        u = controller(t, x)
        log.record(t=t, x=x.copy(), u=u.copy() if hasattr(u, "copy") else u)
        x = integrator(f, t, x, u, dt)
        t += dt
    return log.as_dict()


def coffee_dynamics(t, x, u):
    return -K * (x - X_ROOM)


def no_controller(t, x):
    return np.zeros_like(x)


def analytic_solution(t, x0):
    return X_ROOM + (x0 - X_ROOM) * np.exp(-K * t)


def hook_euler_instability():
    k, e0 = 1.5, 70.0
    for dt in (0.1, 1.6):
        r = 1 - k * dt
        e = e0
        for _ in range(6):
            e *= r


def run_comparison():
    x0 = np.array([90.0])
    t_end, dt_small, dt_big = 15.0, 0.1, 1.6
    data_euler_small = simulate(coffee_dynamics, x0, no_controller, t_end, dt_small, integrator=euler_step)
    data_euler_big = simulate(coffee_dynamics, x0, no_controller, t_end, dt_big, integrator=euler_step)
    data_rk4_big = simulate(coffee_dynamics, x0, no_controller, t_end, dt_big, integrator=rk4_step)
    return data_euler_small, data_euler_big, data_rk4_big


def plot_comparison(data_euler_small, data_euler_big, data_rk4_big):
    # Two panels: top shows the full Euler blow-up, bottom omits the
    # unstable series so matplotlib autoscales to the well-behaved ones.
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
    fig.savefig(OUTPUT_DIR / "integrators.png")


if __name__ == "__main__":
    hook_euler_instability()
    data = run_comparison()
    plot_comparison(*data)
