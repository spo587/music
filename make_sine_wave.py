import subprocess
import os
import math
note_string = ''
import struct
bit = 32
sample_rate = 50000
 
def make_sine_wave(freq,length):
    note_string = ''
    for i in range(0,int(sample_rate/freq)):
        amplitude = (2**bit - 1)/2.0
        offset = (2**bit - 1)/2.0
        phase = math.pi*2*i*freq/sample_rate
        note_string += struct.pack('I',int(round(amplitude*math.sin(phase)+offset)))
     
    multiplier = int(round(length * freq))
    note_string *= multiplier
    return note_string

# for i in range(0,int(sample_rate/(2.0*freq)+1)):
#     note_string+= chr(int(round(255/2.0*math.sin(math.pi*2*i*freq/sample_rate))))

# for i in range(int(sample_rate/(2.0*freq)+1),int(sample_rate/(freq))):
#     note_string += chr(int(round(255/2.0*math.sin(math.pi*2*i*freq/sample_rate)+255)))




# print note_string



if __name__ == '__main__':


    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)
    p.stdin.write(make_sine_wave(200,1.5))



