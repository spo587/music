import subprocess
import os
import math
note_string = ''

## building a sine wave out of characters. change the length of the step to change the frequency of the wave. current 


for i in range(0,505,4):
    note_string += chr(int(round(0.3*126*math.sin(math.pi*i/(2*126))))+80)


note_string *= 1000

p = subprocess.Popen(['sox', '-r', '50000', '-b', '8', '-c', '1', '-t', 'raw', '-s', '-', '-d'], stdin=subprocess.PIPE)
p.stdin.write(note_string)


