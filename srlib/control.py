"""
control.py — controllers, from PID by feel to LQR by optimisation.

Filled in during L0.8 (PID), L3.3 (pole placement), L3.4 (LQR).

The arc of this module is the arc of the whole subject:

    PID             you tune it by feel and it works, and you can't say why
    pole placement  you choose the closed-loop behaviour and solve for the gain
    LQR             you state what you care about, and the optimal gain falls out

Each step trades intuition for structure. None of them replaces the one before.
Real vehicles fly on cascaded PID more often than on anything fancier.
"""
from __future__ import annotations

import numpy as np


class PID:
    """Textbook PID with the practical bits that textbooks skip.

        u = Kp*e + Ki*integral(e) + Kd*de/dt

    Intuition to hold on to (L0.8):
        P  a spring pulling you toward the setpoint. Alone, it wobbles.
        D  a damper. It brakes. It also amplifies sensor noise, which is
           why you differentiate the *measurement*, not the error.
        I  kills constant bias (wind, an off-centre payload). It also winds
           up and overshoots badly the moment the actuator saturates, which
           is why output_limits and anti-windup are not optional extras.

    Filled in: L0.8
    """

    def __init__(
        self,
        kp: float,
        ki: float = 0.0,
        kd: float = 0.0,
        output_limits: tuple[float, float] | None = None,
        derivative_on_measurement: bool = True,
    ) -> None:
        raise NotImplementedError("L0.8")

    def reset(self) -> None:
        """Clear the integral and derivative memory. Call this between runs."""
        raise NotImplementedError("L0.8")

    def update(self, setpoint: float, measurement: float, dt: float) -> float:
        raise NotImplementedError("L0.8")


# --------------------------------------------------------------------------
# State-space design — Level 3
# --------------------------------------------------------------------------

def controllability_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """[B, AB, A^2 B, ...]. Full rank means you can steer every mode.

    If it isn't full rank, no controller of any kind can place those poles,
    and no amount of tuning will save you. Check this before you design.

    Filled in: L3.3
    """
    raise NotImplementedError("L3.3")


def place_poles(A: np.ndarray, B: np.ndarray, desired_poles: np.ndarray) -> np.ndarray:
    """Find K such that the eigenvalues of (A - B K) are the desired poles.

    You'll write this yourself and then check it against MATLAB's place()
    and python-control's place(). If your gains match, you understood it.

    Filled in: L3.3
    """
    raise NotImplementedError("L3.3")


def lqr(A: np.ndarray, B: np.ndarray, Q: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Optimal gain K minimising the cost integral of (x'Qx + u'Ru) dt.

    Stop guessing pole locations. Write down what you care about instead:
    Q penalises state error, R penalises control effort. Big R means a lazy,
    gentle controller; big Q means an aggressive one that will happily saturate
    your motors. Solve the continuous algebraic Riccati equation, and K = R^-1 B' P.

    Filled in: L3.4
    """
    raise NotImplementedError("L3.4")


class CascadedController:
    """Nested loops: each loop's output is the next loop's setpoint.

    Position -> velocity -> attitude -> rate -> motor mixer. Five loops on a
    quadcopter (L1.4). The rule that makes it work: an inner loop must be
    roughly 5x faster than the loop wrapped around it, so the outer loop sees
    a plant that has already settled.

    Filled in: L1.4
    """

    def __init__(self, loops: list[PID]) -> None:
        raise NotImplementedError("L1.4")
