import subprocess
import matplotlib.pyplot as mpl
import os
import math
note_string = ''
import struct
bit = 32

sample_rate = 100000.0

 
def build_sine_wave(freq,duration):
    note_string_ints = []
    for i in range(0,int(duration*freq*sample_rate/freq)):
        amplitude = (2**bit - 1)/2.0
        offset = (2**bit - 1)/2.0
        phase = math.pi*2*i*freq/sample_rate
        note_string_ints.append(int(round(amplitude*math.sin(phase)+offset)))
    return note_string_ints



def make_bytes_wave(note_string_ints):
    l = [struct.pack('I',num) for num in note_string_ints]
    bytes  = ''.join(l)
    return bytes

def combine_two_sine_waves(wave1, wave2):
    note_string_ints = [(x+y)/2.0 for x,y in zip(wave1,wave2)]
    return note_string_ints


def make_sine_wave_sound(freq,duration):
    ints = build_sine_wave(freq,duration)
    bytes = make_bytes_wave(ints)
    return bytes

def make_tone(freq1,freq2,duration,):
    ints = combine_two_sine_waves(build_sine_wave(freq1,duration),build_sine_wave(freq2,duration))
    bytes = make_bytes_wave(ints)
    return bytes



def bytes_to_ints(bytes):
    l =[]
    for i in range(len(bytes)/4):
        print repr(bytes[4*i:4*i+4])
        l.append(struct.unpack('I',bytes[4*i:4*i+4]))

    return l


if __name__ == '__main__':


    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)

    p.stdin.write(make_tone(500,1000,2))




