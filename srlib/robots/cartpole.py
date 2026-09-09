"""
cartpole.py — a pendulum on a cart. The fruit fly of control theory.

Filled in during L3.5. Balanced with LQR in boss fight BF3, then ported to
MuJoCo so you can watch your controller survive real contact physics.

State:
    x        cart position        [m]
    xdot     cart velocity        [m/s]
    theta    pole angle from UP   [rad]
    thetadot pole angular rate    [rad/s]

Input:
    F        horizontal force on the cart [N]

Why this system, and not something friendlier:

    It is UNDERACTUATED — one motor, two degrees of freedom. You cannot
    command the pole directly; you can only move the cart and let the pole
    respond. Every interesting robot is underactuated: a walking robot cannot
    push on the ground it isn't touching, a quadcopter cannot move sideways
    without tilting first. Learn it here where it's four states.

    It is also UNSTABLE about the upright equilibrium, which means the
    linearised A matrix has an eigenvalue in the right half-plane, which
    means it will fall over unless the controller is actively working. That
    makes it an honest test: a broken controller is visibly broken.
"""
from __future__ import annotations

import numpy as np


class CartPole:
    """Cart-pole with the pole measured from vertical (theta = 0 is upright).

    Filled in: L3.5
    """

    def __init__(
        self,
        cart_mass: float = 1.0,    # [kg]
        pole_mass: float = 0.1,    # [kg]
        pole_length: float = 0.5,  # [m] to the centre of mass
        gravity: float = 9.81,
        friction: float = 0.0,
    ) -> None:
        raise NotImplementedError("L3.5")

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Full non-linear dynamics. Filled in: L3.5"""
        raise NotImplementedError("L3.5")

    def linearise(self, x_eq: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
        """Return (A, B) linearised about an equilibrium — upright by default.

        This is the moment L0.4's small-angle approximation earns its keep:
        sin(theta) -> theta, cos(theta) -> 1, and a nasty non-linear system
        becomes a 4x4 matrix you can design against. Then note carefully how
        far from upright that approximation stays honest, because your
        controller will be trusted outside that range eventually.

        Filled in: L3.5
        """
        raise NotImplementedError("L3.5")

    def energy(self, x: np.ndarray) -> float:
        """Total mechanical energy — needed for the swing-up stretch goal in BF3.

        Filled in: BF3 stretch
        """
        raise NotImplementedError("BF3 stretch")
