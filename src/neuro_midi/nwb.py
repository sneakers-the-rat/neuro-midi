from collections.abc import Generator
from pathlib import Path

import h5py
import numpy as np
from numpydantic import NDArray, Shape


def iter_units(
    path: Path, start: int = 0, n: int | None = None
) -> Generator[NDArray[Shape["*"], float]]:
    """
    Iterate the spike times for units in an NWB units dataset
    """
    with h5py.File(str(path), "r") as f:
        units = f.get("/units")
        idx = np.concatenate([np.array([0], dtype=int), units.get("spike_times_index")[:]])
        spike_times = units.get("spike_times")

        if isinstance(n, int):
            iterator = zip(idx[start : start + n], idx[start + 1 : start + n + 1])
        else:
            iterator = zip(idx[start:-1], idx[start + 1 :])

        for start, end in iterator:
            yield spike_times[start:end]
