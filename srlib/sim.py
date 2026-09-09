"""
sim.py — the simulation loop and numerical integration.

Filled in during L0.1 (NumPy for robotics) and L0.2 (discrete time).

The big idea of this module: a robot simulation is just

    while t < t_end:
        u = controller(state)          # decide
        state = integrate(f, state, u, dt)   # let physics happen
        log(t, state, u)               # remember
        t += dt

Everything else in this course is a variation on those four lines.
"""
from __future__ import annotations

from typing import Callable
import numpy as np

# A dynamics function: f(t, x, u) -> xdot
Dynamics = Callable[[float, np.ndarray, np.ndarray], np.ndarray]


def euler_step(f: Dynamics, t: float, x: np.ndarray, u: np.ndarray, dt: float) -> np.ndarray:
    """Advance the state one timestep using forward (explicit) Euler.

    x_{k+1} = x_k + dt * f(t, x_k, u_k)

    The simplest integrator there is, and the one that will bite you in L0.2
    when you make dt too big and watch a perfectly stable spring explode.

    Args:
        f:  dynamics, f(t, x, u) -> xdot
        t:  current time [s]
        x:  current state vector
        u:  current input vector
        dt: timestep [s]

    Returns:
        The state at t + dt.

    Filled in: L0.2
    """
    raise NotImplementedError("L0.2")


def rk4_step(f: Dynamics, t: float, x: np.ndarray, u: np.ndarray, dt: float) -> np.ndarray:
    """Advance the state one timestep using classic 4th-order Runge-Kutta.

    Four evaluations of f per step instead of one, but the error shrinks like
    dt^4 instead of dt. Usually a bargain. You'll measure exactly how much of
    a bargain in L0.2.

    Filled in: L0.2
    """
    raise NotImplementedError("L0.2")


class Logger:
    """Collects named time series during a simulation run.

    Usage:
        log = Logger()
        log.record(t=0.0, z=1.2, z_cmd=1.5, u=0.4)
        ...
        data = log.as_dict()   # {"t": array, "z": array, ...}

    Deliberately dumb. Its only job is to make plotting painless, because
    you cannot debug what you cannot see.

    Filled in: L0.1
    """

    def __init__(self) -> None:
        #raise NotImplementedError("L0.1")
        self.data: dict[str, list[float]] = {}


    def record(self, **kwargs: float) -> None:
        for key, value in kwargs.items():
            # If key doesn't exist, set it to [] then append the value
            self.data.setdefault(key, []).append(value)

    def as_dict(self) -> dict[str, np.ndarray]:
        return {key: np.array(values) for key, values in self.data.items()}
        #raise NotImplementedError("L0.1")


def simulate(
    f: Dynamics,
    x0: np.ndarray,
    controller: Callable[[float, np.ndarray], np.ndarray],
    t_end: float,
    dt: float,
    integrator: Callable = rk4_step,
) -> dict[str, np.ndarray]:
    """Run a closed-loop simulation and return the logged data.

    This is the workhorse. Nearly every lesson from here calls it.

    Filled in: L0.2
    """
    raise NotImplementedError("L0.2")
