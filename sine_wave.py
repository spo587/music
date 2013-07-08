import math
import matplotlib.pyplot as mpl

note_string = []


for i in range(0,505,1):
    note_string.append(int(round(0.3*126*math.sin(math.pi*i/(2*126))))+80)

note_string *= 10
Y = note_string
X = range(len(note_string))

mpl.scatter(X,Y)


mpl.show()
assert False