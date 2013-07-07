import subprocess
import os
import math
note_string = ''
for i in range(33,127,8):
    note_string += chr(int(round(126*math.sin(math.pi*i/(2*126)))))


note_string_reversed = list(note_string)
note_string_reversed.reverse()
for i in range(len(note_string_reversed)):
    note_string += (note_string_reversed[i])


note_string *= 1000
print note_string





# note = 'echo %s | sox -r 50000 -b 8 -c 1 -t raw -s - -d' %note_string
# # # # # #print s
# os.system(note)

