# Guitar-tuner

Guitar tuner is a Python program for tuning a guitar.
It is designed to tune a guitar using only computer and to extend knowledge of digital signal processing.

## Requirements

Numpy and PyAudio are required.

```bash
pip install numpy
```
```bash
pip install PyAudio
```

## Usage

Tuner is set for classic guitar. By default it uses main audio input.
Program starts with info messenge about sampling frequency and max resolution.
Then it starts measuring frequency and printing corresponding notes names with cents.
New notes are printed only when frequency changes.

To check if chosen string is correctly tuned you need to play it and compare output with corresponding note.

## License
[license file](./LICENSE)
