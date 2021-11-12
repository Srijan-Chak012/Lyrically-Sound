import numpy as np

def get_piano_notes():   
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] 
    base_freq = 440 #Frequency of Note A4
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])
    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]
    
    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    # print(note_freqs)
    return note_freqs

def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    t = np.linspace(0, duration, int(sample_rate*duration)) # Time axis
    wave = amplitude*np.sin(2*np.pi*frequency*t)
    return wave
import numpy as np

def apply_overtones(frequency, duration, factor, sample_rate=44100, amplitude=4096):
    '''
    What are overtones?
    These are resonant frequencies that are above the fundamental frequencies - they may or may not be harmonics
    This section will enables us to make harmonies and make full-fledged symphonies of the song later on
    '''

    #this will make an array of tones that have been detected by the fast fourier transform but isn't principal/fundamental frequency
    frequencies = np.minimum(np.array([frequency*(x+1) for x in range(len(factor))]), sample_rate//2)
    amplitudes = np.array([amplitude*x for x in factor])
    
    #this will add harmonies 
    fundamental = get_sine_wave(frequencies[0], duration, sample_rate, amplitudes[0])
    for i in range(1, len(factor)):
        overtone = get_sine_wave(frequencies[i], duration, sample_rate, amplitudes[i])
        fundamental += overtone
    return fundamental

def apply_pedal(note_values, bar_value):
    new_values = []
    start = 0
    while True:
        #returns the cumulative value of array elements in that particular bar, from sum until the end (np.cumsum does this)
        cum_value = np.cumsum(np.array(note_values[start:])) 
        
        #returns the index of the value which is true and satisfies the condition, this based on length of the note itself
        end = np.where(cum_value == bar_value)[0][0] 
        
        if end == 0:
        
            #simply appends the note to the array as the end of the bar has been reached
            new_values += [note_values[start]] 
        
        else:
        
            #is an array of all the notes in the bar for which sustain needs to be applied
            this_bar = np.array(note_values[start:start+end+1]) 

            #adds sustain to the notes accordingly, follows that pattern that the earlier the note comes in the bar, the longer it needs to be sustained
            new_values += [bar_value-np.sum(this_bar[:i]) for i in range(len(this_bar))] 
        
        #after the bar is completed, it moves to the next bar
        start += end+1

        #checks if song has reached the end
        if start == len(note_values):
            break
    return new_values

def get_song_data(music_notes, note_values, bar_value, factor, length, decay, sustain_level, sample_rate=44100, amplitude=4096):
    #obtains frequencies from the database of 88 notes 
    note_freqs = get_piano_notes()
    frequencies = [note_freqs[note] for note in music_notes]

    #depending on user and how much they want to sustain, this line creates a new array of each note and for how long they need to be played
    new_values = apply_pedal(note_values, bar_value)
    
    #total duration of the song
    duration = int(sum(note_values)*sample_rate)

    #casting the numpy array of all the notes to int
    end_idx = np.cumsum(np.array(note_values)*sample_rate).astype(int)
    
    #concatenating the new numpy (int) array 
    start_idx = np.concatenate(([0], end_idx[:-1]))

    #rewriting the end_idx array with the new (sustained) value
    end_idx = np.array([start_idx[i]+new_values[i]*sample_rate for i in range(len(new_values))]).astype(int)
    
    #formatting the numpy array within the structure of duration wherever necessary using np.zeros 
    song = np.zeros((duration,))

    #the final song (array with notes and frequencies)
    for i in range(len(music_notes)):
        this_note = apply_overtones(frequencies[i], new_values[i], factor)
        weights = 1
        song[start_idx[i]:end_idx[i]] += this_note*weights

    song = song*(amplitude/np.max(song))
    return song