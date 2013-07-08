import subprocess
import os
import math
note_string = ''

## building a sine wave out of characters. change the length of the step to change the frequency of the wave. current 

freq = 300.0
sample_rate = 20000.0

for i in range(0,int(sample_rate/freq)):
    note_string+= chr(int(round(255/2.0*math.sin(math.pi*2*i*freq/sample_rate)+255/2.0)))


note_string *= 1000

if __name__ == '__main__':


    p = subprocess.Popen(['sox', '-r', '20000', '-b', '8', '-c', '1', '-t', 'raw', '-s', '-', '-d'], stdin=subprocess.PIPE)
    p.stdin.write(note_string)


