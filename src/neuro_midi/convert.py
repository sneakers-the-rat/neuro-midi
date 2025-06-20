from pathlib import Path
from typing import Any, cast

import mido
import numpy as np
from mido import Message, MidiFile, MidiTrack, bpm2tempo, second2tick
from numpydantic import NDArray, Shape
from tqdm import tqdm

from neuro_midi.nwb import iter_units

TICKS_PER_BEAT = 1000


def timestamps_to_notes(
    array: NDArray[Shape["*"], float],
    note: int,
    duration: float = 1,
    channel: int = 0,
    velocity: int = 64,
    tempo: int = 120,
) -> MidiTrack:
    """
    Convert an array of timestamps (in seconds) to a list of midi events.

    Ticks are delta ticks rather than absolute ticks

    Args:
        array (NDArray[Shape["*"], float]): The 1-D array of timestamps (in seconds).
        note (int): The note to use for the events
        duration (int): The duration of each note in ms -
            the value of the timestamp is treated as the start time,
            and end time is start + duration_ms
        channel (int): MIDI channel to render notes as (0-15)
        velocity (int): Velocity of note (1-128)
        tempo (int): Tempo of track in BPM

    Returns:
        MidiTrack
    """
    array = np.sort(array)
    kwargs = {
        "channel": channel,
        "velocity": velocity,
        "note": note,
    }
    events = []
    # mido expects tempo to be in microseconds per quarter note rather than BPM
    tempo = bpm2tempo(tempo)
    delta_off = second2tick(duration / 1000, TICKS_PER_BEAT, tempo)
    abs_time = 0
    for ts in array:
        # have to use delta ticks here
        on_tick = second2tick(ts, TICKS_PER_BEAT, tempo)
        if on_tick <= abs_time:
            continue
        delta_on = on_tick - abs_time
        events.append(Message("note_on", time=delta_on, **kwargs))
        events.append(Message("note_off", time=delta_off, **kwargs))
        abs_time += delta_on + delta_off

    return MidiTrack(events)


def units_to_midi(
    path: Path,
    tempo: int = 120,
    progress: bool = False,
    start: int = 0,
    n: int | None = None,
    start_note: int = 0,
    merge_tracks: bool = True,
    **kwargs: Any,
) -> MidiFile:
    """
    Iterate over units in an NWB file, creating a MIDI file

    Different spike timeseries are assigned to different notes within different channels,
    incrementing notes from 0-127 and channels from 0-15

    Args:
        path (Path): Path to the NWB file
        tempo (int): Tempo of track in BPM
        start (int): Index of starting unit to begin iteration
        n (int): Number of units to convert starting at start. If None, all units after `start`.
        start_note (int): MIDI note (int 0-127) to start iterating from (middle C is 60)
        merge_tracks (bool): If true, merge all tracks from units into a single track
        **kwargs: forwarded to `timestamps_to_notes`

    """
    tracks = []
    total = None
    if isinstance(n, int):
        total = n - start
    iterator = enumerate(iter_units(path, start=start, n=n))
    if progress:
        iterator = tqdm(iterator, total=total)

    for i, timestamps in iterator:
        note = (i + start_note) % 128
        channel = i // 128
        tracks.append(
            timestamps_to_notes(timestamps, note=note, channel=channel, tempo=tempo, **kwargs)
        )

    if progress:
        iterator = cast(tqdm, iterator)
        iterator.close()

    if merge_tracks:
        tracks = [mido.merge_tracks(tracks)]

    file = MidiFile(ticks_per_beat=TICKS_PER_BEAT, tracks=tracks)
    return file