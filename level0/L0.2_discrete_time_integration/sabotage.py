"""
Lesson 0.2 -- sabotage

Don't read this file hunting for a diff against your srlib/sim.py. Run it
(`python sabotage.py`), open integrators_sabotage.png, and work out what's
wrong FROM THE PLOT ALONE. Then, in your own words in PROGRESS.md, name the
category of bug -- not just "line 20 is wrong".

Self-contained on purpose: it doesn't import srlib or lesson.py, so it runs
regardless of where you've got to on the TODOs.
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# Save next to this script, not wherever the process happened to be launched
# from -- otherwise "python sabotage.py" run from the repo root (or from
# VS Code's default cwd) silently drops the PNG somewhere else.
OUTPUT_DIR = Path(__file__).resolve().parent

K = 1.5
X_ROOM = 20.0


def f(t, x, u):
    return -K * (x - X_ROOM)


def euler_step(f, t, x, u, dt):
    return x + dt * f(t, x, u)


def rk4_step_SUSPECT(f, t, x, u, dt):
    k1 = f(t, x, u)
    k2 = f(t, x, u)
    k3 = f(t, x, u)
    k4 = f(t, x, u)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def run(integrator, dt, t_end=15.0):
    x = np.array([90.0])
    t = 0.0
    ts, xs = [0.0], [x[0]]
    while t < t_end:
        x = integrator(f, t, x, np.zeros(1), dt)
        t += dt
        ts.append(t)
        xs.append(x[0])
    return np.array(ts), np.array(xs)


if __name__ == "__main__":
    dt = 1.6
    t_euler, x_euler = run(euler_step, dt)
    t_rk4, x_rk4 = run(rk4_step_SUSPECT, dt)

    plt.figure(figsize=(7, 5))
    plt.plot(t_euler, x_euler, "o-", label="Euler, dt=1.6")
    plt.plot(t_rk4, x_rk4, "s-", label='"RK4", dt=1.6')
    plt.axhline(X_ROOM, color="gray", linewidth=0.8)
    plt.xlabel("t [s]")
    plt.ylabel("temperature [deg C]")
    plt.title("L0.2 sabotage -- RK4 is supposed to be the stable one here")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "integrators_sabotage.png")
    print(f"Saved {OUTPUT_DIR / 'integrators_sabotage.png'}")
