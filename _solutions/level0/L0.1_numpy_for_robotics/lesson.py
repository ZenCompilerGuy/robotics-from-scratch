"""Lesson 0.1 -- worked solution. See level0/L0.1_numpy_for_robotics/lesson.py
for the exercise version with commentary."""
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


def hook_list_vs_array() -> None:
    x_list = [0.0, 0.0, 0.0]
    v_list = [1.0, 2.0, 3.0]
    dt = 0.1
    try:
        result = x_list + v_list * dt
    except TypeError as e:
        result = f"TypeError: {e}"
    print("x_list + v_list * dt  =", result)
    x_arr = np.array(x_list)
    v_arr = np.array(v_list)
    print("np.array version: x_arr + v_arr * dt =", x_arr + v_arr * dt)


def update_positions(pos: np.ndarray, vel: np.ndarray, dt: float) -> np.ndarray:
    return pos + vel * dt


def speeds_of(vel: np.ndarray) -> np.ndarray:
    return np.linalg.norm(vel, axis=1)


def run_particles(n_particles: int = 4, t_end: float = 5.0, dt: float = 0.05):
    rng = np.random.default_rng(seed=0)
    pos = np.zeros((n_particles, 2))
    vel = rng.uniform(-1.0, 1.0, size=(n_particles, 2))

    log = Logger()
    t = 0.0
    while t < t_end:
        pos = update_positions(pos, vel, dt)
        log.record(t=t, pos=pos.copy(), speed=speeds_of(vel))
        t += dt

    return log.as_dict(), vel


def plot_trajectories(data: dict, vel: np.ndarray) -> None:
    positions = np.stack(data["pos"])
    plt.figure(figsize=(5, 5))
    for i in range(positions.shape[1]):
        plt.plot(positions[:, i, 0], positions[:, i, 1], label=f"particle {i} (v={vel[i].round(2)})")
    plt.scatter([0], [0], c="k", marker="x", label="start")
    plt.legend(fontsize=8)
    plt.axis("equal")
    plt.title("L0.1 -- particle trajectories")
    plt.tight_layout()
    plt.savefig("trajectories.png")


if __name__ == "__main__":
    hook_list_vs_array()
    data, vel = run_particles()
    plot_trajectories(data, vel)
