import subprocess
import os
import math
note_string = ''
import struct
import make_sine_wave as msw 

 
sample_rate = 50000
bit = 32
 

 
class Note(object):
    '''dictionary will specifiy number of half-steps to increment above or below a-440'''
    note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10}
    for note in note_dict.keys():
        note_dict[note + '#'] = note_dict[note] + 1
        note_dict[note + 'b'] = note_dict[note] - 1
        #to-add: doublesharps and flats too


    def __init__(self, name, value):
        '''name=pitch class, a tuple of (alphabet letter, octave). octave = 0 is the first octave 
        above a-440. octave < 0 means number of octaves below a-440.
         value is the note length. value of 1/4.0 = quarter, etc.'''
        self.name = name
        self.value = value

    def parse_length(self):
        length = self.value*4*60/float(tempo)
        return length

    def parse_freq(self):
        half_steps_above_440 = Note.note_dict[self.name[0]]+12*self.name[1]
        freq = 440*2**(float(half_steps_above_440)/12)
        return freq
        
    def play_note(self):
        p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stdin=subprocess.PIPE)
        return p.stdin.write(msw.make_sound(self.parse_freq(),self.parse_length()))

class Tune(object):
    def __init__(self,notes):
        '''notes is a list of Note instances'''
        self.notes = notes

    def play(self):
        # result = self.notes[0].play_note()
        for i in range(len(self.notes)):
            self.notes[i].play_note()
        

ode_firstphrase = Tune([Note(('f',-1),1/2.0),Note(('a',1),1/4.0),Note(('a',1),1/4.0),
                Note(('bb',1),1/4.0), Note(('c',1),1/4.0),Note(('c',1),1/4.0),
                Note(('bb',1),1/4.0),Note(('a',1),1/4.0),Note(('g',0),1/4.0),
                Note(('f',0),1/4.0),Note(('f',0),1/4.0),Note(('g',0),1/4.0),
                Note(('a',1),1/4.0),Note(('a',1),1/4.0+1/8.0),Note(('g',0),1/8.0),Note(('g',0),1/2.0)])


# ode_second_phrase = Tune(ode_firstphrase.notes[1:13]Note(('g',-1),1/4.0+1/8.0)
note1 = Note(('b#',0),1/2.0)
note2 = Note(('b',0),1/2.0)
 
if __name__ == '__main__':
    tempo = 150 #quarter note beats per minute
    ode_firstphrase.play()
    note1.play_note()
    assert False

    
    
