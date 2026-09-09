"""
plotting.py — seeing what your robot is doing.

Filled in during L0.3.

You cannot debug what you cannot see. A controller that "doesn't work" is an
unreadable statement; a plot showing the response oscillating at 4 Hz with
growing amplitude tells you your derivative gain is fighting sensor noise.

Build these once, reuse them thirty times.
"""
from __future__ import annotations

import numpy as np


def time_plot(data: dict[str, np.ndarray], signals: list[str],
              title: str = "", ylabel: str = "") -> None:
    """Plot one or more logged signals against time on a single axis.

    Filled in: L0.3
    """
    raise NotImplementedError("L0.3")


def dashboard(data: dict[str, np.ndarray], groups: list[list[str]],
              title: str = "") -> None:
    """Stacked subplots sharing a time axis — one group of signals per row.

    The standard view for a control run: command vs measurement on top,
    error in the middle, control effort at the bottom. Once you can read
    that layout at a glance, tuning stops being guesswork.

    Filled in: L0.3
    """
    raise NotImplementedError("L0.3")


def phase_portrait(f, xlim: tuple[float, float], ylim: tuple[float, float],
                   density: int = 20) -> None:
    """Vector field of a 2D system — arrows showing where the state is pushed.

    This is what makes `xdot = Ax` stop being algebra. Stable systems have
    arrows spiralling inward; unstable ones spiral out; a saddle does both
    at once, and the inverted pendulum you balance in L3.5 is a saddle.

    Filled in: L0.5
    """
    raise NotImplementedError("L0.5")


def animate_2d(states: np.ndarray, draw_fn, dt: float,
               save_path: str | None = None) -> None:
    """Animate a 2D robot, optionally exporting a GIF into gallery/.

    The GIFs are not decoration — they're your portfolio. An employer will
    watch a five-second GIF of your cart-pole balancing. They will not read
    your controller source.

    Filled in: L0.3
    """
    raise NotImplementedError("L0.3")
