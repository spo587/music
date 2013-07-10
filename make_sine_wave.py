import subprocess
import os
import math
import struct
from collections import defaultdict
import time


bit = 32
sample_rate = 20000.0
wave_peak = (2**bit - 1)/2.0
tempo = 80

def exponential_decay(k,time):
    return math.exp(-k*time)

def linear_decay(k,time):
    return (1 - k*time)

def no_decay(k,time):
    return 1


class Instrument(object):
    def __init__(self,name,overtone_decay_func_dict,overtone_strengths_dict,overtone_constants_dict):
        self.name = name
        self.overtone_decay_func_dict = overtone_decay_func_dict
        self.overtone_constants_dict = overtone_constants_dict
        self.overtone_strengths_dict = overtone_strengths_dict

    def build_sine_waves(self,fund_freq,duration):
        waves = []
        for overtone in self.overtone_strengths_dict.keys():
            wave = build_sine_wave(overtone*fund_freq,duration,self.overtone_constants_dict[overtone],wave_peak*self.overtone_strengths_dict[overtone],self.overtone_decay_func_dict[overtone])
            waves.append(wave)
        #print len(waves)
        return waves

    def combine_waves(self,fund_freq,duration):
        waves = self.build_sine_waves(fund_freq,duration)
        return combine_n_waves(*waves)

    def convert_to_bytes(self,fund_freq,duration):
        note_string_ints = self.combine_waves(fund_freq,duration)
        bytes = convert_to_bytes(note_string_ints)
        return bytes



dict1 = {1:0.5, 2: 0.1, 3: 0.1, 4: 0.05, 5: 0.05, 6: 0.01, 7:0.01, 8: 0.01, 9: 0.01}
dict2 = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.2, 5: 7.0, 6: 12.0, 7: 12.0, 8:7.0, 9: 8.0}
dict3 = {}
for i in range(1,5):
    dict3[i] = linear_decay
for i in range(5,14):
    dict3[i] = exponential_decay

crappy_instrument = Instrument('crappy',dict3,dict1,dict2)

dict4 = {}
for key in dict1.keys():
    dict4[key]=0


silence = Instrument('silent',dict3,dict4,dict2)

class Line(object):
    def __init__(self,notes_value_pairs,instrument):
        '''notes_value_pairs will be a list each element has form [('a',-1),1/4.0]'''
        self.notes_value_pairs = notes_value_pairs
        self.instrument = instrument

    def make_tones(self):
        tones = []
        for notes_value_pair in notes_value_pairs:
            tones.append(Tone(notes_value_pair[0],notes_value_pair[1]))
        return tones

class Chord(object):
    def __init__(self,tones):
        self.tones = tones
        #self.bytes = self.make_bytes()

    def combine_tones(self):
        waves = [tone.instrument.combine_waves(tone.fund_freq,tone.duration) for tone in self.tones]
        return combine_n_waves(*waves)
    
    def convert_to_bytes(self):
        note_string_ints = self.combine_tones()
        return convert_to_bytes(note_string_ints)


class Tone(object):
    note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10}
    for note in note_dict.keys():
        note_dict[note + '#'] = note_dict[note] + 1
        note_dict[note + 'b'] = note_dict[note] - 1
    def __init__(self, name, note_value, instrument=crappy_instrument):
        '''overtone_strengths_dict is a dictionary of the relative initial amplitudes of the fundamental and its overtones
        overtone_decay_dict is a dict of the time constants of the fundamental and its overtones'''
        self.name = name
        self.note_value = note_value
        self.fund_freq = self.parse_freq()
        self.duration = self.parse_duration()
        self.overtone_strengths_dict = instrument.overtone_strengths_dict
        self.overtone_constants_dict = instrument.overtone_constants_dict 
        self.overtone_decay_func_dict = instrument.overtone_decay_func_dict
        self.instrument = instrument

    def parse_duration(self):
        duration = self.note_value*4*60/float(tempo)
        return duration

    def parse_freq(self):
        half_steps_above_440 = Tone.note_dict[self.name[0]]+12*self.name[1]
        fund_freq = 440*2**(float(half_steps_above_440)/12)
        return fund_freq
    def convert_to_bytes(self):
        return self.instrument.convert_to_bytes(self.fund_freq,self.duration)


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
    def convert_to_bytes(self):
        ints = self.apply_decay_func()
        bytes = convert_to_bytes(ints)
        return bytes        

def build_sine_wave(freq, duration, time_constant=0.0, max_amplitude=wave_peak, decay_function=exponential_decay):
    note_string_ints = []
    for i in range(0,int(duration*freq*sample_rate/freq)):
        offset = (2**bit - 1)/2.0
        phase = math.pi*2*i*freq/sample_rate
        note_string_ints.append(int(round(max_amplitude*decay_function(time_constant,i/sample_rate)*math.sin(phase)+offset)))
    return note_string_ints




def convert_to_bytes(note_string_ints):
    l = [struct.pack('I',num) for num in note_string_ints]
    bytes  = ''.join(l)
    return bytes


def combine_n_waves(*waves):
    note_string_ints = [sum(tup)/float(len(waves)) for tup in zip(*waves)]
    return note_string_ints
def play(list_of_things):
    bytes = combine_things(list_of_things)
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return p.stdin.write(bytes)

def play2(list_of_ints):
    bytes = convert_to_bytes(list_of_ints)
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return p.stdin.write(bytes)


def combine_things(list_of_things):
    """
    >>> combine_byte([chord1.to_bytes(),chord2.to_bytes])"""
    return ''.join([thing.convert_to_bytes() for thing in list_of_things])

def combine_things_ints(list_of_things):
    l = []
    for thing in list_of_things:
        l += thing.instrument.combine_waves(thing.fund_freq,thing.duration)
    return l


if __name__ == '__main__':
    t_0 = time.time()
    tune1 = bach_herzliebster()
    t_1 = time.time()
    print t_1 - t_0
    play2(tune1)
    
    

    
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
    # assert combine_two_sine_waves(build_sine_wave(400,2), build_sine_wave(800,2)) == combine_n_waves(build_sine_wave(400,2),build_sine_wave(800,2))
    
    # p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)

    # # p.stdin.write(make_tone_fundamental_four_overtones(440,2))
    # p.stdin.write(make_sine_wave_sound(440,2,3.0))




# def make_sine_wave_sound(freq,duration,time_constant=0,max_amplitude=wave_peak):
#     ints = build_sine_wave(freq,duration,time_constant)
#     bytes = make_bytes_wave(ints)
#     return bytes






