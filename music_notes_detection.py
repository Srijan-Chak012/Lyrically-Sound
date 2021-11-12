import numpy as np
import wave
import os
import struct
import matplotlib.pyplot as plt
import sys

def extract_sound(audio_file, file_length, sound):
	for i in range(file_length):
	    wdata = audio_file.readframes(1)
        # print(sys.getsizeof(wdata))
	    data = struct.unpack("<h", wdata)
	    sound[i] = int(data[0])

def plot_sound(audio_file, sound):
	sound = np.divide(sound, float(2**15)) 
	plt.plot(sound)
	plt.savefig('img/soundplot_canonviolin.jpg')
	plt.show()

def assign(freq):
	# frequency database
	note = 0
	name = np.array(["C4", "C4#", "D4", "D4#", "E4", "F4", "F4#", "G4", "G4#", "A4", "A4#", "B4", "C5", "C5#", "D5", "D5#", "E5", "F5", "F5#", "G5", "G5#", "A5", "A5#", "B5"])
	frequencies = np.array([261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77])

    # searching for matched frequencies
	for i in range(0, frequencies.size-1):
	    if(freq < frequencies[0]):
	        note = name[0]
	        break
	    if(freq > frequencies[-1]):
	        note = name[-1]
	        break
	    if freq >= frequencies[i] and frequencies[i+1] >= freq:
	        if freq-frequencies[i] < (frequencies[i+1]-frequencies[i])/2:
	            note = name[i]
	        else:
	            note = name[i+1]
	        break

	return note

def note_detect(audio_file):
	file_length = audio_file.getnframes()
	f_s = audio_file.getframerate()  # sampling frequency
	sound = np.zeros(file_length) 

	extract_sound(audio_file, file_length, sound)

	plot_sound(audio_file, sound)
	counter = audio_file.getnchannels()

    # fourier transformation from numpy module
	fourier = np.fft.fft(sound)
	fourier = np.absolute(fourier)
	imax = np.argmax(fourier[0:int(file_length/2)])  # index of max element

	plt.plot(fourier)
	plt.savefig('img/fourier_canonviolin.jpg')
	plt.show()

    # peak detection
	i_begin = -1
	threshold = 0.3 * fourier[imax]
	for i in range(0, imax+100):
	    if fourier[i] >= threshold:
	        if(i_begin == -1):
	            i_begin = i
	    if(i_begin != -1 and fourier[i] < threshold):
	        break
	i_end = i
	imax = np.argmax(fourier[0:i_end+100])

    # formula to convert index into sound frequency
	freq = (imax*f_s)/(file_length*counter)
	# print(freq) 
	note = assign(freq)
    

import music21

if __name__ == "__main__":

	path = os.getcwd()
	file_name = path + "/wav/canon_violin.wav"
	audio_file = wave.open(file_name)
	Detected_Note = note_detect(audio_file)
	# print("\n\tDetected Note = " + str(Detected_Note))
	score = music21.converter.parse('midi/canon_violin.midi')
	key = score.analyze('key')
	print(key.tonic.name, key.mode)

