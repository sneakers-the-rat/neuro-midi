from pathlib import Path

import click

from neuro_midi.convert import units_to_midi


@click.group("neuro-midi")
def main() -> None:
    """Convert neuro data types to MIDI!"""


@main.group("nwb")
def nwb() -> None:
    """Convert from NWB to MIDI"""


@nwb.command("units")
@click.option("-p", "--path", type=click.Path(exists=True), required=True, help="Path to NWB file")
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False),
    required=False,
    help="output .midi file",
    default=None,
)
@click.option(
    "-d", "--duration", type=float, help="Duration of each note in milliseconds", default=1
)
@click.option("-v", "--velocity", type=int, help="Velocity of each note, 0-127", default=64)
@click.option("-t", "--tempo", type=int, help="Tempo of the midi file in BPM", default=120)
@click.option("-s", "--start", type=int, help="Index of unit to start iterating over", default=0)
@click.option(
    "-n",
    type=int,
    help="Number of units to convert, starting from --start. If None, convert all",
    default=None,
)
@click.option(
    "--note", type=int, help="number of note (0-127) to start from, (middle C is 60)", default=0
)
def nwb_units(
    path: Path,
    output: Path | None = None,
    duration: float = 1,
    velocity: int = 64,
    tempo: int = 120,
    start: int = 0,
    n: int | None = None,
    note: int = 0,
) -> None:
    """
    Convert NWB units (spike times for individual neurons) to MIDI notes
    """
    path = Path(path)
    if output is None:
        output = path.with_suffix(".midi")

    midi_file = units_to_midi(
        path=path,
        duration=duration,
        velocity=velocity,
        tempo=tempo,
        progress=True,
        start=start,
        n=n,
        start_note=note,
    )
    with open(output, "wb") as f:
        midi_file.save(file=f)

    click.echo(f"Wrote midi file to {output}")
