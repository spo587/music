import subprocess
import matplotlib.pyplot as mpl
import os
import math
note_string = ''
import struct
bit = 32

sample_rate = 100000.0

 
def make_sine_wave(freq,length):
    note_string_ints = []
    for i in range(0,int(length*sample_rate/freq)):
        amplitude = (2**bit - 1)/2.0
        offset = (2**bit - 1)/2.0
        phase = math.pi*2*i*freq/sample_rate
        note_string_ints.append(int(round(amplitude*math.sin(phase)+offset)))
    return note_string_ints

y = make_sine_wave(440,10)
x = range(len(y))

mpl.scatter(x,y)
mpl.show()
# var1 = make_sine_wave(440)
# y = var1
# x = range(len(var1))
# mpl.scatter(x,y)
# mpl.show()

def make_bytes_wave(note_string_ints):
    l = [struct.pack('I',num) for num in note_string_ints]
    bytes  = ''.join(l)
    return bytes

def bytes_to_ints(bytes):
    l =[]
    for i in range(len(bytes)/4):
        print repr(bytes[4*i:4*i+4])
        l.append(struct.unpack('I',bytes[4*i:4*i+4]))

    return l


def make_sound(freq,length):
    ints = make_sine_wave(freq,length)
    bytes = make_bytes_wave(ints)
    return bytes




if __name__ == '__main__':


    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)

    p.stdin.write(make_sound(455,1000))




