import subprocess
import os
import math
note_string = ''

## building a sine wave out of characters. change the length of the step to change the frequency of the wave. current 
## current frequency is 416 Hz.
for i in range(33,127,8):
    note_string += chr(int(round(126*math.sin(math.pi*i/(2*126)))))


note_string_reversed = list(note_string)
note_string_reversed.reverse()
for i in range(len(note_string_reversed)):
    note_string += (note_string_reversed[i])



note_string *= 1000
## print to a new file or comment out
print note_string




## this part doesn't work, throws weird errors at me

# note = 'echo %s | sox -r 50000 -b 8 -c 1 -t raw -s - -d' %note_string
# os.system(note)

