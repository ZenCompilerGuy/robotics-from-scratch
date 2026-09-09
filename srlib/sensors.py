"""
sensors.py — realistic fake sensors. Because sensors lie.

Filled in during L0.9, extended in L2.x and L5.x.

Every sensor in this module corrupts the truth in a specific, physical way,
and each way of lying has a specific cure:

    white noise   -> averaging / low-pass filtering (costs you lag)
    bias          -> calibration, or estimate it as part of the state
    drift         -> a second sensor that doesn't drift (this is Level 2)
    quantisation  -> nothing much; live with it
    latency       -> account for it in the filter, or it eats your phase margin
    dropout       -> your filter must survive a missing measurement

If you only ever test controllers on perfect data, you have not tested them.
"""
from __future__ import annotations

import numpy as np


class Gyroscope:
    """Measures body angular rate. Low noise, but biased and slowly drifting.

    Trustworthy over a second. Useless over a minute.

    Filled in: L0.9
    """

    def __init__(self, noise_std: float, bias: np.ndarray, drift_rate: float = 0.0,
                 rng: np.random.Generator | None = None) -> None:
        raise NotImplementedError("L0.9")

    def measure(self, omega_true_b: np.ndarray, dt: float) -> np.ndarray:
        raise NotImplementedError("L0.9")


class Accelerometer:
    """Measures specific force in the body frame: a_body - g, not acceleration.

    That distinction is the whole lesson. At rest it reads gravity, which gives
    you roll and pitch for free. The moment the robot accelerates, that free
    lunch is over — which is exactly why L2.2 fails and L2.3 exists.

    Filled in: L0.9
    """

    def __init__(self, noise_std: float, bias: np.ndarray,
                 rng: np.random.Generator | None = None) -> None:
        raise NotImplementedError("L0.9")

    def measure(self, accel_true_w: np.ndarray, R_wb: np.ndarray) -> np.ndarray:
        raise NotImplementedError("L0.9")


class Magnetometer:
    """Measures the local magnetic field in the body frame. Gives you yaw.

    Noisy, and easily corrupted by any lump of metal or current-carrying wire
    nearby — which on a real drone means the motors.

    Filled in: L0.9
    """

    def __init__(self, noise_std: float, field_w: np.ndarray,
                 rng: np.random.Generator | None = None) -> None:
        raise NotImplementedError("L0.9")

    def measure(self, R_wb: np.ndarray) -> np.ndarray:
        raise NotImplementedError("L0.9")


class RangeFinder:
    """Distance to the nearest obstacle along a ray. Used for the Level 5 capstone.

    Filled in: L5.2
    """

    def __init__(self, noise_std: float, max_range: float,
                 dropout_prob: float = 0.0,
                 rng: np.random.Generator | None = None) -> None:
        raise NotImplementedError("L5.2")

    def measure(self, pose: np.ndarray, world_map) -> float:
        raise NotImplementedError("L5.2")


# --------------------------------------------------------------------------
# Simple filters — the naive cures, so you can feel why they're not enough
# --------------------------------------------------------------------------

class MovingAverage:
    """N-sample moving average. Smooths noise, and adds roughly N/2 samples of lag.

    That trade — smoothness bought with lag — is the reason the Kalman filter
    was invented. Feel the pain here so Level 4 lands.

    Filled in: L0.9
    """

    def __init__(self, window: int) -> None:
        raise NotImplementedError("L0.9")

    def update(self, x: float) -> float:
        raise NotImplementedError("L0.9")


class LowPass:
    """First-order low-pass (exponential) filter: y += alpha * (x - y).

    One line, one tuning knob, and it is everywhere in real robot firmware.

    Filled in: L0.9
    """

    def __init__(self, alpha: float, y0: float = 0.0) -> None:
        raise NotImplementedError("L0.9")

    def update(self, x: float) -> float:
        raise NotImplementedError("L0.9")
