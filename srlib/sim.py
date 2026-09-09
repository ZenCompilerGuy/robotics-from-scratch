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
    # TODO(L0.2): one line.
    return x + dt * f(t, x, u)
    #   k1 = f(t, x, u)
    #   return x + dt * k1
    #raise NotImplementedError("L0.2")


def rk4_step(f: Dynamics, t: float, x: np.ndarray, u: np.ndarray, dt: float) -> np.ndarray:
    """Advance the state one timestep using classic 4th-order Runge-Kutta.

    Four evaluations of f per step instead of one, but the error shrinks like
    dt^4 instead of dt. Usually a bargain. You'll measure exactly how much of
    a bargain in L0.2.

    Filled in: L0.2
    """
    # TODO(L0.2): the four stage evaluations (see notes.md for the derivation
    # of why this exact weighting), each using f(t, x, u):
    k1 = f(t,        x,             u)
    k2 = f(t + dt/2, x + dt/2 * k1, u)
    k3 = f(t + dt/2, x + dt/2 * k2, u)
    k4 = f(t + dt,   x + dt   * k3, u)
    return x + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    #raise NotImplementedError("L0.2")


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
        self.data: dict[str, list[float]] = {}

    def record(self, **kwargs: float) -> None:
        for key, value in kwargs.items():
            self.data.setdefault(key, []).append(value)

    def as_dict(self) -> dict[str, np.ndarray]:
        return {key: np.array(values) for key, values in self.data.items()}


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
    # TODO(L0.2): the loop from this module's own docstring. Log the state
    # BEFORE advancing it (so the first logged entry is x0 at t=0), then step:
    log = Logger()
    x = x0.copy()
    t = 0.0
    while t < t_end:
        u = controller(t, x)
        log.record(t=t, x=x.copy(), u=u.copy() if hasattr(u, "copy") else u)
        x = integrator(f, t, x, u, dt)
        t += dt
    return log.as_dict()
    #raise NotImplementedError("L0.2")
