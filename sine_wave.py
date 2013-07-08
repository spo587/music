import math
import matplotlib.pyplot as mpl
import sys

note_string = []

sample_rate = 50000.0
freq = 400.0
for i in range(0,int(sample_rate/freq)+1):
    note_string.append(int(round(255/2.0*math.sin(math.pi*2*i*freq/(sample_rate))+255/2.0)))


Y = note_string
X = range(len(note_string))

mpl.scatter(X,Y)


mpl.show()
sys.exit()
