# neuro-midi
some simple utilities to convert neural data to MIDI

not intended for general public use, just for a side project :)

more docs soon but for now try downloading a dataset
(e.g. [this one](https://api.dandiarchive.org/api/assets/eb9e50e0-3980-4b7e-86b9-995f79bab797/download/)),
installing the package (e.g. from github, `python -m pip install git+https://github.com/sneakers-the-rat/neuro-midi`),
and using the CLI:

```shell
neuro-midi nwb units -p ./sub-0_ses-20230901_ecephys.nwb -n 10 --note 60
```

```
Usage: neuro-midi nwb units [OPTIONS]

  Convert NWB units (spike times for individual neurons) to MIDI notes

Options:
  -p, --path PATH         Path to NWB file  [required]
  -o, --output PATH       output .midi file
  -d, --duration FLOAT    Duration of each note in milliseconds
  -v, --velocity INTEGER  Velocity of each note, 0-127
  -t, --tempo INTEGER     Tempo of the midi file in BPM
  -s, --start INTEGER     Index of unit to start iterating over
  -n INTEGER              Number of units to convert, starting from --start.
                          If None, convert all
  --note INTEGER          number of note (0-127) to start from, (middle C is
                          60)
  --help                  Show this message and exit.

```