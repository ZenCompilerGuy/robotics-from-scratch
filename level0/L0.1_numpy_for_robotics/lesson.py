"""
Lesson 0.1 -- NumPy for robotics
=================================

The one idea: a NumPy array is a vector or matrix, not a list. It obeys
different rules than a Python list under + and *, and those rules
(broadcasting) are what let you write "move every particle by its own
velocity" as one line instead of a loop over indices.

Run this file top to bottom (`python lesson.py`) and read the printed
output before you scroll on. Fill in the two TODOs below before the plot
at the bottom will run without crashing.
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

import sys
from pathlib import Path

# lesson.py lives two folders below the repo root; python lesson.py only
# puts THIS folder on sys.path, not the root where srlib/ lives. pytest
# gets this for free from conftest.py -- direct script runs don't, so we
# do it by hand. Same trick, every lesson from here on.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from srlib.sim import Logger


# ---------------------------------------------------------------------------
# Part 1 -- the hook: lists lie to you
# ---------------------------------------------------------------------------

def hook_list_vs_array() -> None:
    """Show what happens when you translate `x = x + v*dt` from MATLAB
    habits straight into Python using lists instead of arrays."""
    x_list = [0.0, 0.0, 0.0]
    v_list = [1.0, 2.0, 3.0]
    dt = 0.1

    try:
        result = x_list + v_list * dt  # the "natural" MATLAB-habit line
    except TypeError as e:
        result = f"TypeError: {e}"

    print("x_list + v_list * dt  =", result)
    print("  (expected something like [0.1, 0.2, 0.3] if this behaved like a vector)")
    print()

    x_arr = np.array(x_list)
    v_arr = np.array(v_list)
    print("np.array version: x_arr + v_arr * dt =", x_arr + v_arr * dt)


# ---------------------------------------------------------------------------
# Part 2 -- TODO: vectorised state update (fill these in, no loops allowed)
# ---------------------------------------------------------------------------

def update_positions(pos: np.ndarray, vel: np.ndarray, dt: float) -> np.ndarray:
    """Advance every particle's position by one timestep.

    pos: shape (N, 2) -- N particles, each an (x, y) position
    vel: shape (N, 2) -- each particle's own constant velocity
    dt:  scalar timestep

    Returns the updated (N, 2) position array. This should be ONE line --
    no loop over particles. Broadcasting does the work because pos and vel
    already share a shape.
    """
    # TODO(L0.1): replace the next line
    return pos + vel * dt


def speeds_of(vel: np.ndarray) -> np.ndarray:
    """Return the speed (scalar magnitude) of every particle's velocity.

    vel: shape (N, 2)
    Returns: shape (N,) -- one speed per particle.

    Hint: np.linalg.norm(vel, axis=1)
    """
    # TODO(L0.1): replace the next line
    return np.linalg.norm(vel, axis=1)



# ---------------------------------------------------------------------------
# Part 3 -- the reusable loop skeleton (you'll see this exact shape ~30 more
# times across this course -- decide, integrate, log, advance time)
# ---------------------------------------------------------------------------

def run_particles(n_particles: int = 4, t_end: float = 5.0, dt: float = 0.05):
    rng = np.random.default_rng(seed=0)
    pos = np.zeros((n_particles, 2))
    vel = rng.uniform(-1.0, 1.0, size=(n_particles, 2))

    log = Logger()
    t = 0.0
    while t < t_end:
        pos = update_positions(pos, vel, dt)              # integrate
        log.record(t=t, pos=pos.copy(), speed=speeds_of(vel))  # log (see notes.md re: .copy())
        t += dt

    return log.as_dict(), vel


def plot_trajectories(data: dict, vel: np.ndarray) -> None:
    positions = np.stack(data["pos"])  # shape (T, N, 2)
    plt.figure(figsize=(5, 5))
    for i in range(positions.shape[1]):
        plt.plot(
            positions[:, i, 0], positions[:, i, 1],
            label=f"particle {i} (v={vel[i].round(2)})",
        )
    plt.scatter([0], [0], c="k", marker="x", label="start")
    plt.legend(fontsize=8)
    plt.axis("equal")
    plt.title("L0.1 -- particle trajectories")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig("trajectories.png")
    print("Saved trajectories.png -- open it and compare to your prediction.")


if __name__ == "__main__":
    hook_list_vs_array()
    print()
    print("Before running the sim: with 4 particles starting at the origin, each")
    print("with its own random velocity, sketch (paper or in your head) what the")
    print("4 trajectories should look like after 5 seconds. Then run this file.")
    print()
    data, vel = run_particles()
    plot_trajectories(data, vel)
