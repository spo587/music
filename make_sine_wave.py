import subprocess
import matplotlib.pyplot as mpl
import os
import math
note_string = ''
import struct
bit = 32

sample_rate = 100000.0

def exponential_decay(k,t):
    return math.exp(-k*t)



 
def build_sine_wave(freq, duration, max_amplitude=(2**bit - 1)/2.0):
    note_string_ints = []
    for i in range(0,int(duration*freq*sample_rate/freq)):
        offset = (2**bit - 1)/2.0
        phase = math.pi*2*i*freq/sample_rate
        note_string_ints.append(int(round(max_amplitude*math.sin(phase)+offset)))
    return note_string_ints

def decayed_sine_wave(note_string_ints,k):
    for i in range(len(note_string_ints)):
        note_string_ints[i] = note_string_ints[i]*exponential_decay(k,i/sample_rate)
    return note_string_ints




def make_bytes_wave(note_string_ints):
    l = [struct.pack('I',num) for num in note_string_ints]
    bytes  = ''.join(l)
    return bytes

def combine_two_sine_waves(wave1, wave2):
    note_string_ints = [(x+y)/2.0 for x,y in zip(wave1,wave2)]
    return note_string_ints

def combine_five_sine_waves(waves):
    '''waves a list of five sine waves from build function above'''
    note_string_ints = [(x+y+z+a+b)/5.0 for x,y,z,a,b in zip(waves[0],waves[1],waves[2],waves[3],waves[4])]
    return note_string_ints


def make_tone_fundamental_four_overtones(freq,duration,relative_powers=[0.5,0.1,0.1,0.05,0.03]):
    '''relative powers a list of the relative powers of the four overtones'''
    wave1 = build_sine_wave(freq,duration,relative_powers[0]*(2**bit-1)/2.0)
    wave2 = build_sine_wave(freq*2,duration,relative_powers[1]*(2**bit - 1)/2.0)
    wave3 = build_sine_wave(freq*3,duration,relative_powers[2]*(2**bit - 1)/2.0)
    wave4 = build_sine_wave(freq*4,duration,relative_powers[3]*(2**bit - 1)/2.0)
    wave5 = build_sine_wave(freq*5,duration,relative_powers[4]*(2**bit - 1)/2.0)
    waves = [wave1,wave2,wave3,wave4,wave5]
    ints = combine_five_sine_waves(waves)
    bytes = make_bytes_wave(ints)
    return bytes



def make_sine_wave_sound(freq,duration):
    ints = build_sine_wave(freq,duration)
    bytes = make_bytes_wave(ints)
    return bytes

def make_decayed_sine_wave_sound(freq,duration,k):
    ints = decayed_sine_wave(build_sine_wave(freq,duration),k)
    bytes = make_bytes_wave(ints)
    return bytes

def make_tone_two_sine_waves(freq1,freq2,duration,relative_power=0.1):
    ints = combine_two_sine_waves(build_sine_wave(freq1,duration),build_sine_wave(freq2,duration,relative_power*(2**bit - 1)/2.0))
    bytes = make_bytes_wave(ints)
    return bytes



def bytes_to_ints(bytes):
    l =[]
    for i in range(len(bytes)/4):
        print repr(bytes[4*i:4*i+4])
        l.append(struct.unpack('I',bytes[4*i:4*i+4]))

    return l


if __name__ == '__main__':

    # wave = build_sine_wave(440,0.1)

    # decayed = decayed_sine_wave(wave,1.0)
    # y = decayed
    # x = range(len(y))
    # mpl.scatter(x,y)
    # mpl.show()
    
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)

    # p.stdin.write(make_tone_fundamental_four_overtones(440,2))
    p.stdin.write(make_decayed_sine_wave_sound(440,2,3.0))




