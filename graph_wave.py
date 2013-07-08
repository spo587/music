
import matplotlib.pyplot as mpl
import math
note_string = ''

## building a sine wave out of characters. change the length of the step to change the frequency of the wave. current 

freq = 300.0
sample_rate = 20000.0

for i in range(0,int(sample_rate/freq)+1):
    note_string+= chr(int(round(255/2.0*math.sin(math.pi*2*i*freq/sample_rate)+255/2.0)))


note_string *= 10

l = [ord(c) for c in note_string]

x = range(len(l))
y = l
mpl.scatter(x,y)
mpl.show()