import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
plt.style.use('seaborn-dark')
import requirements

# Get middle C frequency
note_freqs = requirements.get_piano_notes()
frequency = note_freqs['C4']

# Pure sine wave
sine_wave = requirements.get_sine_wave(frequency, duration=2, amplitude=2048)
wavfile.write('wav/pure_c.wav', rate=44100, data=sine_wave.astype(np.int16))

def plot_wave():
    sample_rate, middle_c = wavfile.read('wav/pure_c.wav')

    # Plot sound wave
    plt.plot(middle_c[500:2500])
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Sound Wave of Middle C on Piano')
    plt.grid()
    plt.savefig('img/soundwave_middlec.jpg')
    plt.show()

def FFT():

    sample_rate, middle_c = wavfile.read('wav/pure_c.wav')
    t = np.arange(middle_c.shape[0])
    freq = np.fft.fftfreq(t.shape[-1])*sample_rate
    sp = np.fft.fft(middle_c) 

    # Plot spectrum
    plt.plot(freq, abs(sp.real))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Spectrum of Middle C Recording on Piano')
    plt.xlim((0, 2000))
    plt.grid()
    plt.savefig('img/fft_middlec.jpg')
    plt.show()

def scale():
    scale = ['D4','E4','F#4','G4','A4','B4','C#5','D5']
    note_values = [0.5]*8
    factor = [1]
    length = [0]
    decay = [0]
    sustain_level = 0.0

    scale_sustain = requirements.get_song_data(scale, note_values, bar_value=0.5, factor=factor, length=length, decay=decay, sustain_level=sustain_level)
    wavfile.write('wav/scale.wav', 44100, scale_sustain.astype(np.int16))
    print("Scale produced!")

plot_wave()
FFT()
scale()