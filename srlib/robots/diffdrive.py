"""
diffdrive.py — a differential-drive ground robot. The Level 5 capstone platform.

Filled in during L5.2, used through the capstone.

State (pose):
    x, y     position in the world [m]
    theta    heading               [rad]

Input:
    v        forward velocity      [m/s]
    omega    turn rate             [rad/s]
    (or left/right wheel speeds — convert with wheel_to_body)

Why a ground robot for the probabilistic level: uncertainty in 3 states is
something you can actually draw. You will plot a thousand particles on a map
and see the belief split into two clumps and then collapse onto the right one,
and that picture is worth more than any derivation.

The thing to notice in L5.2: propagate a Gaussian through this model and the
result is NOT a Gaussian. Drive forward with uncertain heading and the cloud
of possible positions bends into a banana. Every Kalman filter applied to a
wheeled robot is quietly pretending that banana is an ellipse. Sometimes that's
fine. Sometimes it's why your robot thinks it's in the wrong room.
"""
from __future__ import annotations

import numpy as np


class DiffDrive:
    """Kinematic differential-drive robot.

    Filled in: L5.2
    """

    def __init__(
        self,
        wheel_radius: float = 0.05,   # [m]
        wheel_base: float = 0.30,     # [m] between wheel contact points
        max_speed: float = 1.0,       # [m/s]
    ) -> None:
        raise NotImplementedError("L5.2")

    def wheel_to_body(self, omega_left: float, omega_right: float) -> tuple[float, float]:
        """Wheel angular speeds -> (v, omega). Filled in: L5.2"""
        raise NotImplementedError("L5.2")

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Kinematic model: xdot = v cos(theta), ydot = v sin(theta), thetadot = omega.

        Filled in: L5.2
        """
        raise NotImplementedError("L5.2")

    def sample_motion(self, pose: np.ndarray, u: np.ndarray, dt: float,
                      alpha: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Draw ONE sample from p(x_t | u_t, x_{t-1}) — the probabilistic motion model.

        Note what this is and isn't: it does not return a mean and a covariance,
        it returns a single plausible next pose. Call it a thousand times and
        the cloud of results IS the distribution. That shift — from propagating
        a distribution to sampling from it — is the whole idea behind the
        particle filter.

        Filled in: L5.2
        """
        raise NotImplementedError("L5.2")
