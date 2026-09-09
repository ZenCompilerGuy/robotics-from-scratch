# The Logger class as it should end up inside srlib/sim.py after L0.1.
# Paste this in to replace the three NotImplementedError bodies.

class Logger:
    def __init__(self) -> None:
        self._data: dict[str, list] = {}

    def record(self, **kwargs: float) -> None:
        for key, value in kwargs.items():
            self._data.setdefault(key, []).append(value)

    def as_dict(self) -> dict[str, np.ndarray]:
        return {key: np.array(values) for key, values in self._data.items()}
