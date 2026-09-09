"""
Lesson 0.1 -- sabotage

Don't read this file line by line looking for the diff against lesson.py.
Run it (`python sabotage.py`), open trajectories_sabotage.png, and work out
what's wrong FROM THE PLOT ALONE. Then, in your own words in PROGRESS.md,
name the category of NumPy mistake it is -- not just "line 23 is wrong".

Self-contained on purpose: it doesn't import your lesson.py, so it runs
regardless of where you've got to on the TODOs.
"""
import numpy as np
import matplotlib.pyplot as plt


def update_positions(pos: np.ndarray, vel: np.ndarray, dt: float) -> np.ndarray:
    return pos + vel * dt


def run_particles(n_particles: int = 4, t_end: float = 5.0, dt: float = 0.05):
    rng = np.random.default_rng(seed=0)
    pos = np.zeros((n_particles, 2))
    vel = rng.uniform(-1.0, 1.0, size=(n_particles, 2))

    vel = vel[0]  # looks like a harmless simplification. it is not.

    positions = [pos.copy()]
    t = 0.0
    while t < t_end:
        pos = update_positions(pos, vel, dt)
        positions.append(pos.copy())
        t += dt

    return np.stack(positions), vel


def plot_trajectories(positions: np.ndarray) -> None:
    plt.figure(figsize=(5, 5))
    for i in range(positions.shape[1]):
        plt.plot(positions[:, i, 0], positions[:, i, 1], label=f"particle {i}")
    plt.scatter([0], [0], c="k", marker="x", label="start")
    plt.legend(fontsize=8)
    plt.axis("equal")
    plt.title("L0.1 sabotage -- what's wrong here?")
    plt.savefig("trajectories_sabotage.png")
    print("Saved trajectories_sabotage.png")


if __name__ == "__main__":
    positions, vel = run_particles()
    plot_trajectories(positions)
