"""
quad.py — a 6-DOF quadcopter, built from Newton-Euler.

Filled in during L1.1. Flown through L1.2-L1.5 and boss fight BF1.

State (13 or 12 elements depending on your attitude representation):
    p_w      position in world      [3]
    v_w      velocity in world      [3]
    R_wb     attitude              [3x3]  (or Euler [3])
    omega_b  body angular rate      [3]

Inputs:
    four motor speeds, which the mixer turns into
    one collective thrust (body -z) and three body torques.

The physics is short enough to fit on one page:

    m * a_w    = R_wb @ [0, 0, -T] + m*g_w        Newton, in the world frame
    I * omegadot_b = tau_b - omega_b x (I omega_b) Euler, in the body frame

The second term of the second equation — the gyroscopic cross product — is the
one everybody drops, and it's why a fast-spinning drone doesn't behave the way
your linear intuition says it should.

Assumptions we make, and where they bite (write these in your notes):
    - thrust is proportional to motor speed squared, instantly (no motor lag)
    - no aerodynamic drag, no ground effect, no blade flapping
    - rigid body, symmetric inertia (I diagonal)
    - flat earth, constant gravity
"""
from __future__ import annotations

import numpy as np


class Quadcopter:
    """A quadcopter in X configuration.

    Filled in: L1.1
    """

    def __init__(
        self,
        mass: float = 1.0,            # [kg]
        arm_length: float = 0.25,     # [m] motor to centre
        inertia: np.ndarray | None = None,   # [3] diagonal Ixx Iyy Izz [kg m^2]
        thrust_coeff: float = 3.0e-6,
        torque_coeff: float = 1.0e-7,
        gravity: float = 9.81,
    ) -> None:
        raise NotImplementedError("L1.1")

    def mixer(self, motor_speeds: np.ndarray) -> tuple[float, np.ndarray]:
        """Four motor speeds -> (collective thrust, body torque vector).

        This is a 4x4 matrix. Its rows encode the geometry: which motors spin
        which way, which arm is where. Getting a sign wrong here produces a
        drone that flips instantly on take-off, which is a rite of passage.

        Filled in: L1.1
        """
        raise NotImplementedError("L1.1")

    def inverse_mixer(self, thrust: float, torque_b: np.ndarray) -> np.ndarray:
        """(thrust, torque) -> four motor speeds. The mixer, inverted.

        This is the last block in the control cascade — the point where your
        careful control maths finally becomes four numbers sent to four ESCs.

        Filled in: L1.1
        """
        raise NotImplementedError("L1.1")

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """xdot = f(t, x, u), ready to hand to srlib.sim.simulate.

        Filled in: L1.1
        """
        raise NotImplementedError("L1.1")
