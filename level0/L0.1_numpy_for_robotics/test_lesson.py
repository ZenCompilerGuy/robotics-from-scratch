"""
Tests for Lesson 0.1 -- NumPy for robotics.

Run from the repo root:  pytest level0/L0.1_numpy_for_robotics/ -v

These check real numerical properties, not exact string/print matches.
Green means your broadcasting and your Logger are doing the right thing.
"""
import numpy as np

from srlib.sim import Logger
from lesson import update_positions, speeds_of


def test_logger_records_multiple_signals_as_arrays():
    log = Logger()
    for i in range(5):
        log.record(t=i * 0.1, z=float(i) ** 2)
    data = log.as_dict()

    assert set(data.keys()) == {"t", "z"}
    assert isinstance(data["t"], np.ndarray)
    assert len(data["t"]) == 5
    np.testing.assert_allclose(data["z"], [0.0, 1.0, 4.0, 9.0, 16.0])


def test_logger_preserves_recording_order():
    log = Logger()
    log.record(t=0.0)
    log.record(t=0.1)
    log.record(t=0.2)
    data = log.as_dict()
    np.testing.assert_allclose(data["t"], [0.0, 0.1, 0.2])


def test_update_positions_matches_loop_reference():
    rng = np.random.default_rng(1)
    pos = rng.uniform(-1, 1, size=(6, 2))
    vel = rng.uniform(-1, 1, size=(6, 2))
    dt = 0.05

    result = update_positions(pos, vel, dt)

    # Ground truth from an explicit Python loop -- slow, but unambiguous.
    expected = np.zeros_like(pos)
    for i in range(pos.shape[0]):
        expected[i] = pos[i] + vel[i] * dt

    np.testing.assert_allclose(result, expected)


def test_update_positions_preserves_shape():
    pos = np.zeros((10, 2))
    vel = np.ones((10, 2))
    result = update_positions(pos, vel, dt=0.1)

    # The classic list-concatenation failure mode would silently change this
    # to shape (20,) instead of (10, 2). Broadcasting must not collapse or
    # extend the array.
    assert result.shape == (10, 2)


def test_update_positions_each_particle_uses_its_own_velocity():
    pos = np.zeros((3, 2))
    vel = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]])
    result = update_positions(pos, vel, dt=1.0)

    # If velocity got broadcast/indexed wrong, every row would end up
    # identical. Each particle must keep its own direction.
    assert not np.allclose(result[0], result[1])
    assert not np.allclose(result[1], result[2])
    np.testing.assert_allclose(result, vel)  # dt=1, pos=0 => result == vel


def test_speeds_of_matches_norm_definition():
    vel = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 1.0]])
    result = speeds_of(vel)

    expected = np.array([5.0, 0.0, np.sqrt(2)])
    np.testing.assert_allclose(result, expected)


def test_speeds_of_returns_one_value_per_particle():
    vel = np.random.default_rng(2).uniform(-1, 1, size=(7, 2))
    result = speeds_of(vel)
    assert result.shape == (7,)
