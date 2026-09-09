"""
rotations.py — frames, rotation matrices, Euler angles, DCM propagation.

Filled in during L0.6 (2D and frames) and L0.7 (3D, DCM, Rodrigues).

Read this before you write a line:

    Roughly 80% of robotics bugs are frame bugs. Not maths errors — frame
    errors. A vector expressed in the body frame used as though it were in
    the world frame. Every function here uses an explicit naming convention
    and you should adopt it everywhere:

        R_ab   rotates a vector FROM frame b INTO frame a
        v_b    a vector expressed in frame b

    so that   v_a = R_ab @ v_b   reads left to right and the b's cancel.
    If your subscripts don't cancel, you have a bug. This one convention
    will save you hours.

Frames used in this course:
    w  world / inertial (NED: x North, y East, z Down)
    b  body (x forward, y right, z down)
"""
from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------------
# 2D — L0.6
# --------------------------------------------------------------------------

def rot2(theta: float) -> np.ndarray:
    """2x2 rotation matrix for angle theta [rad], counter-clockwise positive.

    Filled in: L0.6
    """
    raise NotImplementedError("L0.6")


# --------------------------------------------------------------------------
# 3D elementary rotations — L0.7
# --------------------------------------------------------------------------

def rot_x(phi: float) -> np.ndarray:
    """Rotation about the x axis (roll) by phi [rad]. Filled in: L0.7"""
    raise NotImplementedError("L0.7")


def rot_y(theta: float) -> np.ndarray:
    """Rotation about the y axis (pitch) by theta [rad]. Filled in: L0.7"""
    raise NotImplementedError("L0.7")


def rot_z(psi: float) -> np.ndarray:
    """Rotation about the z axis (yaw) by psi [rad]. Filled in: L0.7"""
    raise NotImplementedError("L0.7")


# --------------------------------------------------------------------------
# Direction Cosine Matrix <-> Euler angles — L0.7
# --------------------------------------------------------------------------

def dcm_from_euler(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """Build R_wb from ZYX (yaw-pitch-roll) Euler angles.

    ZYX means: yaw first about world z, then pitch about the new y, then roll
    about the newest x. Order matters — rotations do not commute, and proving
    that to yourself with two 90-degree turns of a book is L0.7's hook.

    Returns:
        R_wb, the 3x3 matrix taking body-frame vectors into the world frame.

    Filled in: L0.7
    """
    raise NotImplementedError("L0.7")


def euler_from_dcm(R: np.ndarray) -> tuple[float, float, float]:
    """Recover (roll, pitch, yaw) from a DCM. Watch for gimbal lock at |pitch| = 90 deg.

    Filled in: L0.7
    """
    raise NotImplementedError("L0.7")


def skew(v: np.ndarray) -> np.ndarray:
    """Skew-symmetric matrix of a 3-vector, so that skew(a) @ b == cross(a, b).

    Small function, load-bearing everywhere: it's how a cross product becomes
    a matrix, which is how angular velocity becomes a rotation update.

    Filled in: L0.7
    """
    raise NotImplementedError("L0.7")


def dcm_propagate(R: np.ndarray, omega_b: np.ndarray, dt: float) -> np.ndarray:
    """Integrate a DCM forward given body angular rate, using Rodrigues.

        R_{k+1} = R_k * exp(skew(omega_b) * dt)

    This is how a gyroscope becomes an attitude estimate. It is also how that
    estimate drifts, which is the entire reason Level 2 exists.

    Filled in: L0.7
    """
    raise NotImplementedError("L0.7")


def orthonormalise(R: np.ndarray) -> np.ndarray:
    """Nudge a nearly-orthonormal matrix back onto SO(3).

    Floating-point error accumulates every propagation step until R's rows
    are no longer unit length or mutually perpendicular, and your "rotation"
    quietly starts stretching vectors. This fixes it.

    Filled in: L2.3
    """
    raise NotImplementedError("L2.3")


def is_rotation(R: np.ndarray, tol: float = 1e-9) -> bool:
    """True if R is a valid rotation matrix: R @ R.T == I and det(R) == +1.

    Your tests will lean on this constantly.

    Filled in: L0.7
    """
    raise NotImplementedError("L0.7")
