import subprocess
import os
import math
import struct
from collections import defaultdict

bit = 32
sample_rate = 50000.0
wave_peak = (2**bit - 1)/2.0
tempo = 60

class Chord(object):
    def __init__(self,tones):
        self.tones = tones
        self.bytes = self.make_bytes()

    def combine_tones(self):
        waves = [tone.combine_waves() for tone in self.tones]
        return combine_n_sine_waves(*waves)
    
    def make_bytes(self):
        note_string_ints = self.combine_tones()
        return make_bytes_wave(note_string_ints)




class Tone(object):
    note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10}
    for note in note_dict.keys():
        note_dict[note + '#'] = note_dict[note] + 1
        note_dict[note + 'b'] = note_dict[note] - 1
    def __init__(self, name, note_value, overtone_strengths_dict, overtone_constants_dict, overtone_decay_func_dict):
        '''overtone_strengths_dict is a dictionary of the relative initial amplitudes of the fundamental and its overtones
        overtone_decay_dict is a dict of the time constants of the fundamental and its overtones'''
        self.name = name
        self.note_value = note_value
        self.fund_freq = self.parse_freq()
        self.duration = self.parse_duration()
        self.overtone_strengths_dict = overtone_strengths_dict
        self.overtone_constants_dict = overtone_constants_dict 
        self.overtone_decay_func_dict = overtone_decay_func_dict
        self.bytes = self.make_waves_into_bytes()

    def parse_duration(self):
        duration = self.note_value*4*60/float(tempo)
        return duration

    def parse_freq(self):
        half_steps_above_440 = Tone.note_dict[self.name[0]]+12*self.name[1]
        fund_freq = 440*2**(float(half_steps_above_440)/12)
        return fund_freq
    def build_sine_waves(self):
        waves = []
        for overtone in self.overtone_strengths_dict.keys():
            wave = build_sine_wave(overtone*self.fund_freq,self.duration,self.overtone_constants_dict[overtone],wave_peak*self.overtone_strengths_dict[overtone],self.overtone_decay_func_dict[overtone])
            waves.append(wave)
        #print len(waves)
        return waves

    def combine_waves(self):
        waves = self.build_sine_waves()
        return combine_n_sine_waves(*waves)

    def make_waves_into_bytes(self):
        note_string_ints = self.combine_waves()
        bytes = make_bytes_wave(note_string_ints)
        return bytes


def play(bytes):
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)
    return p.stdin.write(bytes)


def combine_bytes(list_of_bytes):
    """
    Retsdfa

    >>> combine_byte([chord1.to_bytes(),chord2.to_bytes])"""
    return sum(list_of_bytes,'')






def exponential_decay(k,time):
    return math.exp(-k*time)

def linear_decay(k,time):
    return (1 - k*time)

def no_decay(k,time):
    return 1

 
class Sine_wave(object):
    def __init__(self,freq,duration,decay_func):
        self.freq = freq
        self.duration = duration
        self.decay_func = decay_func
        self.bytes = self.make_bytes()

    def build_wave_amplitude_constant(self):
        note_string_ints = build_sine_wave(self.freq,self.duration,decay_function=no_decay)
        return note_string_ints

    def apply_decay_func(self):
        note_string_ints = self.build_wave_amplitude_constant()
        for i in range(len(note_string_ints)):
            note_string_ints[i] = self.decay_func(i/sample_rate)*note_string_ints[i]
        return note_string_ints
    def make_bytes(self):
        ints = self.apply_decay_func()
        bytes = make_bytes_wave(ints)
        return bytes




         

def build_sine_wave(freq, duration, time_constant=0, max_amplitude=wave_peak, decay_function=exponential_decay):
    note_string_ints = []
    for i in range(0,int(duration*freq*sample_rate/freq)):
        offset = (2**bit - 1)/2.0
        phase = math.pi*2*i*freq/sample_rate
        note_string_ints.append(int(round(max_amplitude*decay_function(time_constant,i/sample_rate)*math.sin(phase)+offset)))
    return note_string_ints


def make_bytes_wave(note_string_ints):
    l = [struct.pack('I',num) for num in note_string_ints]
    bytes  = ''.join(l)
    return bytes


def combine_n_sine_waves(*waves):
    note_string_ints = [sum(tup)/float(len(waves)) for tup in zip(*waves)]
    return note_string_ints






# dict4 = {1:0.0, 2:0.0, 3:1.0, 4:1.0, 5:1.0, 6:1.0, 7:1.0}
# dict5 = defaultdict(int)
# dict6 = {}
# for i in range(1,8):
#     dict6[i] = no_decay

# tone3 = Tone(200,1,dict4,dict5,dict6)
# tone4 = tone3
# tone5 = Tone(200*1.5,1, dict4,dict5,dict6)
# tone6 = tone5

# class decay_function(object):
#     def __init__(self,num_divisions,time_cutoffs, function_dict):


# def decay_func_1(time):
#     if time < 0.2:
#         return 5*time
#     elif time < 0.4:
#         return math.exp(-5*(time-0.2))
#     else:
#         return math.exp(-5*(0.4-0.2)) - 0.1*(time-0.4)

# def decay_func_2(time):
#     if time < 0.2:
#         return 5*time
#     elif time < 0.4:
#         return 5*0.2 - 3*(time-0.2)
#     else:
#         return 0.4 - 0.1*(time-0.4)

# sine1 = Sine_wave(440,4,decay_func_2)




if __name__ == '__main__':
    dict1 = {1:0.5, 2: 0.1, 3: 0.1, 4: 0.05, 5: 0.05, 6: 0.3, 7:0.2, 8: 0.1, 9: 0.1, 10: 0.1, 11: 0.1, 12: 0.4, 13: 0.2}
    dict2 = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.2, 5: 7.0, 6: 12.0, 7: 12.0, 8:15.0, 9: 10.0, 10: 10.0, 11: 7.0, 12: 6.0, 13: 7.0}
    dict3 = {}
    for i in range(1,5):
        dict3[i] = linear_decay
    for i in range(5,14):
        dict3[i] = exponential_decay
    tone_a_quarter = Tone(('a',-1),1/4.0,dict1,dict2, dict3)

    tone_e_quarter = Tone(('e',-2),1/4.0,dict1,dict2,dict3)

    # tone_fsharp_quarter = Tone(('f#',-2),1/4.0,dict1,dict2,dict3)

    # tone_e_half = Tone(('e',-2),1/2.0,dict1,dict2,dict3)

    # tone_csharp_quarter = Tone(('c#',-1),1/4.0,dict1,dict2,dict3)

    # tone_b_quarter = Tone(('b',-1),1/4.0,dict1,dict2,dict3)

    # tone_a_whole = Tone(('a',-1),1.0,dict1,dict2, dict3)

    tone_bass_a_quarter = Tone(('a',-2),1.0,dict1,dict2, dict3)

    tone_bass_csharp_qarter = Tone(('c#',-2),1/4.0,dict1,dict2,dict3)

    tone_bass_d_quarter = Tone(('d',-2),1/4.0,dict1,dict2,dict3)

    tone_bass_csharp_half = Tone(('c#',-2),1/2.0,dict1,dict2,dict3)

    tone_bass_a_whole = Tone(('a',-2),1/1.0,dict1,dict2, dict3)

    chord1 = Chord([tone_a_quarter,tone_bass_a_quarter])

    chord2 = Chord([tone_bass_csharp_qarter,tone_e_quarter])

    # chord3 = Chord([tone_bass_d_quarter,tone_fsharp_quarter])

    # chord4 = Chord([tone_e_half,tone_bass_csharp_half])

    # chord5 = Chord([tone_csharp_quarter,tone_e_quarter])

    # chord6 = Chord([tone_b_quarter,tone_e_quarter])

    chord7 = Chord([tone_bass_a_whole,tone_a_whole])
    tempo = 100
    tune1 = combine_bytes([chord1.bytes,chord2,bytes])
    play(tune1)
    # play(chord1.bytes)
    # play(chord1.bytes)
    # play(chord1.bytes)
    # play(chord2.bytes)
    # play(chord3.bytes)
    # play(chord3.bytes)
    # play(chord4.bytes)
    # play(chord5.bytes)
    # play(chord5.bytes)
    # play(chord6.bytes)
    # play(chord6.bytes)
    # play(chord7.bytes)

    # play(tone1.bytes)
    # play(tone1.bytes)
    # play(tone1.bytes)
    # play(tone2.bytes)
    # play(tone3.bytes)
    # play(tone3.bytes)
    # play(tone4.bytes)
    # play(tone5.bytes)
    # play(tone5.bytes)
    # play(tone6.bytes)
    # play(tone6.bytes)
    # play(tone7.bytes)

    # wave = build_sine_wave(440,0.1)

    # decayed = decayed_sine_wave(wave,1.0)
    # y = decayed
    # x = range(len(y))
    # mpl.scatter(x,y)
    # mpl.show()
    # assert combine_two_sine_waves(build_sine_wave(400,2), build_sine_wave(800,2)) == combine_n_sine_waves(build_sine_wave(400,2),build_sine_wave(800,2))
    
    # p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)

    # # p.stdin.write(make_tone_fundamental_four_overtones(440,2))
    # p.stdin.write(make_sine_wave_sound(440,2,3.0))




# def make_sine_wave_sound(freq,duration,time_constant=0,max_amplitude=wave_peak):
#     ints = build_sine_wave(freq,duration,time_constant)
#     bytes = make_bytes_wave(ints)
#     return bytes






