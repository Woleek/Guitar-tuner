import numpy as np
import pyaudio as pa

# MIN_NOTE and MAX_NOTE are set for classic guitar
# SAMPLES_PER_FRAME and FRAMES_PER_FFT should be exp of 2 to allow usage of FFT
MIN_NOTE = 40               # E2 - highest frequency note
MAX_NOTE = 64               # E4 - lowest frequency note
FS = 22000                  # Sampling rate [Hz]
SAMPLES_PER_FRAME = 2048    # Samples per frame
FRAMES_PER_FFT = 16         # FTT from how many frames

# The quantities are calculated on the basis of the constants above
# If the number of samples per FFT is increased, size of the frequency step decreases
# (this also increases the resolution)
# The signal is divided into frames because we don’t want to lose any information
SAMPLES_PER_FFT = SAMPLES_PER_FRAME*FRAMES_PER_FFT
RESOLUTION = float(FS)/SAMPLES_PER_FFT

# List of notes
NOTES = 'C C# D D# E F F# G G# A A# B'.split()

# The conversion of frequency into notes is based on 
# A4(MIDI number 69 and frequency 440,000 Hz)
def freq_to_number(fn): return 12*np.log2(fn/440.0) + 69
def number_to_freq(m): return (2.0**((m-69)/12.0))*440
def numer_to_note(n): return NOTES[n % 12] + str(n/12-1)
def cents(n, n0): return round((n-n0)*100)

def note_to_fft(n): return number_to_freq(n)/RESOLUTION

# Minimum and maximum index in FFT for selected notes
index_min = max(0, int(np.floor(note_to_fft(MIN_NOTE-1))))
index_max = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fft(MAX_NOTE+1))))

# Prepare buffer for FFT
buf = np.zeros(shape=SAMPLES_PER_FFT,
               dtype=np.float32)
num_frames = 0

# Initialize audio
stream = pa.PyAudio().open(format=pa.paInt16,
                           channels=1,
                           rate=FS,
                           input=True,
                           frames_per_buffer=SAMPLES_PER_FRAME)
stream.start_stream()

# Create a Hanning window.
# The application of the window is intended to reduce the leakage 
# of the spectrum in the initial values of the transformation
window = np.hanning(SAMPLES_PER_FFT)

# Initial text
print('Sampling at ', FS, 'Hz with max resolution of ', RESOLUTION, 'Hz')

# A loop that runs as long as the data is received from the original audio input
prev_freq = 1
while stream.is_active():

    # Adjust buffer and enter new data
    buf[:-SAMPLES_PER_FRAME] = buf[SAMPLES_PER_FRAME:]
    buf[-SAMPLES_PER_FRAME:] = np.frombuffer(buffer=stream.read(SAMPLES_PER_FRAME),
                                             dtype=np.int16)

    # FFT is started on the window buffer
    fft = np.fft.rfft(buf * window)

    # Maximum response frequency within the signal spectrum
    freq = (np.abs(fft[index_min:index_max]).argmax() + index_min) * RESOLUTION

    # Assign the frequency to the number of the nearest note
    n = freq_to_number(freq)
    number = int(round(n))

    # Output after buffer overflow and change of frequency 
    num_frames += 1
    if (num_frames >= FRAMES_PER_FFT) & (prev_freq != freq):
        print('freq: {:7.3f} Hz    note: {:3.3s} {:+3d} cents'.format(
            freq, numer_to_note(number), cents(n, number)))
        prev_freq = freq
