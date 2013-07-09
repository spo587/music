import subprocess
import matplotlib.pyplot as mpl
import os
import math
import struct
bit = 32

sample_rate = 100000.0

wave_peak = (2**bit - 1)/2.0


class Tone(object):
    def __init__(self, fund_freq, duration, overtone_strengths_dict, overtone_decay_dict):
        '''overtone_strengths_dict is a dictionary of the relative initial amplitudes of the fundamental and its overtones
        overtone_decay_dict is a dict of the time constants of the fundamental and its overtones'''
        self.fund_freq = fund_freq
        self.duration = duration
        self.overtone_strengths_dict = overtone_strengths_dict
        self.overtone_decay_dict = overtone_decay_dict 

    def build_sine_waves(self):
        waves = []
        for overtone in self.overtone_strengths_dict.keys():
            wave = build_sine_wave(overtone*self.fund_freq,self.duration,self.overtone_decay_dict[overtone],wave_peak*self.overtone_strengths_dict[overtone])
            waves.append(wave)
        print len(waves)
        return waves

    def combine_waves(self):
        waves = self.build_sine_waves()
        return combine_n_sine_waves(*waves)

    def make_waves_into_bytes(self):
        note_string_ints = self.combine_waves()
        bytes = make_bytes_wave(note_string_ints)
        return bytes

    def play_tone(self):
        p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)
        return p.stdin.write(self.make_waves_into_bytes())



def exponential_decay(k,t):
    return math.exp(-k*t)

 
def build_sine_wave(freq, duration, time_constant=0, max_amplitude=wave_peak):
    note_string_ints = []
    for i in range(0,int(duration*freq*sample_rate/freq)):
        offset = (2**bit - 1)/2.0
        phase = math.pi*2*i*freq/sample_rate
        note_string_ints.append(int(round(max_amplitude*exponential_decay(time_constant,i/sample_rate)*math.sin(phase)+offset)))
    return note_string_ints


def make_bytes_wave(note_string_ints):
    l = [struct.pack('I',num) for num in note_string_ints]
    bytes  = ''.join(l)
    return bytes


def combine_n_sine_waves(*waves):
    note_string_ints = [sum(tup)/float(len(waves)) for tup in zip(*waves)]
    return note_string_ints



def make_sine_wave_sound(freq,duration,time_constant=0,max_amplitude=wave_peak):
    ints = build_sine_wave(freq,duration,time_constant)
    bytes = make_bytes_wave(ints)
    return bytes

dict1 = {1:0.5, 2: 0.1, 3: 0.1, 4: 0.05, 5: 0.15, 6: 0.3}
dict2 = {1: 1.0, 2: 1.5, 3: 2.0, 4: 2.0, 5: 4.0, 6: 4.0}
tone1 = Tone(440,3,dict1,dict2)




def bytes_to_ints(bytes):
    l =[]
    for i in range(len(bytes)/4):
        print repr(bytes[4*i:4*i+4])
        l.append(struct.unpack('I',bytes[4*i:4*i+4]))

    return l


if __name__ == '__main__':
    tone1.play_tone()
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




# def make_tone_fundamental_four_overtones(freq,duration,relative_powers=[0.5,0.1,0.1,0.05,0.03]):
#     '''relative powers a list of the relative powers of the four overtones'''
#     wave1 = build_sine_wave(freq,duration,relative_powers[0]*wave_peak)
#     wave2 = build_sine_wave(freq*2,duration,relative_powers[1]*wave_peak)
#     wave3 = build_sine_wave(freq*3,duration,relative_powers[2]*wave_peak)
#     wave4 = build_sine_wave(freq*4,duration,relative_powers[3]*wave_peak)
#     wave5 = build_sine_wave(freq*5,duration,relative_powers[4]*wave_peak)
#     waves = [wave1,wave2,wave3,wave4,wave5]
#     ints = combine_five_sine_waves(waves)
#     bytes = make_bytes_wave(ints)
#     return bytes


# def make_tone_two_sine_waves(freq1,freq2,duration,relative_power=0.1):
#     ints = combine_two_sine_waves(build_sine_wave(freq1,duration),build_sine_wave(freq2,duration,relative_power*(2**bit - 1)/2.0))
#     bytes = make_bytes_wave(ints)
#     return bytes

