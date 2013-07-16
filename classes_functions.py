import subprocess
import os
import math
import struct
from collections import defaultdict
import time

## TODO: 
##  make different instruments
## make sample_rate an input parameter?
## VOICING: either between different lines, or notes within a line/within a vertical element/chord?
## make it so that you can write chords in a single line too
bit = 32
sample_rate = 5000.0
wave_peak = (2**bit - 1)/2.0
tempo = 180
global_key = 310/4.0 #e-flat

class Instrument(object):
    def __init__(self,name,overtone_decay_func_dict,overtone_strengths_dict,overtone_constants_dict,overtone_onset_dict):
        self.name = name
        self.overtone_decay_func_dict = overtone_decay_func_dict
        self.overtone_constants_dict = overtone_constants_dict
        self.overtone_strengths_dict = overtone_strengths_dict
        self.overtone_onset_dict = overtone_onset_dict

    def build_sine_waves(self,fund_freq,duration):
        waves = []
        for overtone in self.overtone_strengths_dict.keys():
            wave = build_sine_wave(overtone*fund_freq,duration,self.overtone_onset_dict[overtone],self.overtone_constants_dict[overtone],wave_peak*self.overtone_strengths_dict[overtone],self.overtone_decay_func_dict[overtone])
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

class Line(object):
    def __init__(self,notes_value_pairs,instrument):
        '''notes_value_pairs will be a list each element has form ['a',-1,1/4.0]'''
        self.notes_value_pairs = notes_value_pairs
        self.instrument = instrument

    def make_tones(self):
        tones = []
        for notes_value_pair in self.notes_value_pairs:
            tones.append(Tone(notes_value_pair[0],notes_value_pair[1],notes_value_pair[2],self.instrument))
        return tones

class Line_steps(Line):
    '''for this class, notes_value_pairs has a different form, simple, a list of list of ints/floats. each inner
    list corresponds to one tone'''
    def make_tones(self):
        tones = []
        for notes_value_pair in self.notes_value_pairs:
            tones.append(Just_tempered_tone(notes_value_pair[0],notes_value_pair[1],notes_value_pair[2],self.instrument))
        return tones

class Tone(object):
    note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10,'rest':0}
    for note in note_dict.keys():
        note_dict[note + '#'] = note_dict[note] + 1
        note_dict[note + 'b'] = note_dict[note] - 1
    def __init__(self, name, octave, note_value, instrument):
        ''''''
        self.name = name
        self.octave = octave
        self.note_value = note_value
        self.fund_freq = self.parse_freq()
        self.duration = self.parse_duration()
        self.overtone_strengths_dict = instrument.overtone_strengths_dict
        self.overtone_constants_dict = instrument.overtone_constants_dict 
        self.overtone_decay_func_dict = instrument.overtone_decay_func_dict
        self.instrument = instrument


    def parse_duration(self):
        return self.note_value*60/float(tempo)

    def parse_freq(self):
        if self.name == 'rest':
            return 0
        half_steps_above_440 = Tone.note_dict[self.name]+12*self.octave
        fund_freq = 440*2**(float(half_steps_above_440)/12)
        return fund_freq

    def convert_to_bytes(self):
        return self.instrument.convert_to_bytes(self.fund_freq,self.duration)

class Just_tempered_tone(Tone):
    scale_degree_dict = {5:1.5,4:4/3.0,3:5/4.0,2:9/8.0,1:1,6:5/3.0,7:3/2.0*(5/4.0)}
    for degree in scale_degree_dict.keys():
        scale_degree_dict[degree+0.5] = scale_degree_dict[degree]*(25/24.0)
    scale_degree_dict['m3'] = 6/5.0
    scale_degree_dict['m7'] = 3/2.0*6/5.0
    def __init__(self,scale_degree,octaves_above,note_value,instrument, key=global_key):
        self.key = key
        self.scale_degree = scale_degree
        self.octaves_above = octaves_above
        self.note_value = note_value
        self.duration = self.parse_duration()
        self.fund_freq = self.parse_freq()
        self.instrument = instrument

    def parse_freq(self):
        if self.scale_degree == 'rest':
            return 0
        
        #try:
        fund_freq = self.key * Just_tempered_tone.scale_degree_dict[self.scale_degree] * (2**self.octaves_above)
        #except KeyError:
         #   print self.scale_degree,Just_tempered_tone.scale_degree_dict
        return fund_freq


class Sine_wave(object):
    def __init__(self,freq,duration,decay_func):
        self.freq = freq
        self.duration = duration
        self.decay_func = decay_func
        self.bytes = self.make_bytes()

    def build_wave_amplitude_constant(self):
        note_string_ints = build_sine_wave(self.freq,self.duration,offset_time=0.0, decay_function=no_decay)
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

def exponential_decay(k,time):
    return math.exp(-k*time)

def linear_decay(k,time):
    return (1 - k*time)

def no_decay(k,time):
    return 1

def immediate(time,offset_time):
    return 1

def linear_onset(time,offset_time):
    return time/float(offset_time)
    


def build_sine_wave(freq, duration, offset_time=0.01,time_constant=0.0, max_amplitude=wave_peak, decay_function=exponential_decay,onset_function=linear_onset):
    note_string_ints = []
    if freq == 0:
        return [0 for i in range(int(round(sample_rate*duration)))]
    max_time = int(round(offset_time * sample_rate))
    shift = (2**bit - 1)/2.0
    for i in range(0, max_time): 
        phase = math.pi*2*i*freq/sample_rate
        note_string_ints.append(int(round(max_amplitude*onset_function(i,max_time)*math.sin(phase)+shift)))

    for i in range(max_time,int(duration*sample_rate)):
        
        phase = math.pi*2*i*freq/sample_rate
        to_append = int(round(max_amplitude*decay_function(time_constant,(i-max_time)/sample_rate)*math.sin(phase)+shift))
        if decay_function(time_constant,(i-max_time)/sample_rate) < 0:
            note_string_ints.append(0)
        else:
            note_string_ints.append(int(round(max_amplitude*decay_function(time_constant,(i-max_time)/sample_rate)*math.sin(phase)+shift)))
    return note_string_ints

def convert_to_bytes(note_string_ints):
    l = [struct.pack('I',num) for num in note_string_ints]
    bytes  = ''.join(l)
    return bytes

def combine_n_waves(*waves):
    note_string_ints = [sum(tup)/float(len(waves)) for tup in zip(*waves)]
    return note_string_ints

def play2(list_of_ints):
    bytes = convert_to_bytes(list_of_ints)
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write(bytes) 

def write_to_file(list_of_ints,file_name):
    bytes = convert_to_bytes(list_of_ints)
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', 'boomtown.raw'], stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write(bytes)
    p.stdin.close()
    #p.wait()
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-e', 'unsigned-integer', 'boomtown.raw', file_name+'.wav'], stdin=subprocess.PIPE)


def combine_things_ints(list_of_things):
    l = []
    for thing in list_of_things:
        l += thing.instrument.combine_waves(thing.fund_freq,thing.duration)
    return l


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


if __name__ == '__main__':
    l1 = build_sine_wave(440,1.5,time_constant=1.0,decay_function=linear_decay)
    l2 = [item for item in l1 if item > 4294967295]
    print l2
    play2(l1)
    
# def combine_things(list_of_things):
#     """
#     >>> combine_byte([chord1.to_bytes(),chord2.to_bytes])"""
#     return ''.join([thing.convert_to_bytes() for thing in list_of_things])


# def play(list_of_things):
#     bytes = combine_things(list_of_things)
#     p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#     return p.stdin.write(bytes)


    # def transpose_tones(self,num_halfsteps):
    #     l = self.make_tones()
    #     for tone in l:
    #         tone.fund_freq *= (2**num_halfsteps/12.0)
    #     return l

