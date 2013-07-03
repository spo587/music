import subprocess
import os

 
class Note(object):
    '''dictionary will specifiy number of half-steps to increment above or below a-440'''
    note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10}
    for note in note_dict.keys():
        note_dict[note + '#'] = note_dict[note] + 1
        note_dict[note + 'b'] = note_dict[note] - 1
        #to-add: doublesharps and flats too

    def __init__(self, name, value):
        '''name=pitch class, a tuple of (alphabet letter, octave). value is the note length value 1/4.0 = quarter, etc.'''
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
        s = 'play -n synth %s sine %s' % (self.parse_length(), self.parse_freq())
        return os.system(s)

class Tune(object):
    def __init__(self,notes):
        '''notes is a list of Note instances'''
        self.notes = notes

    def play(self):
        result = self.notes[0].play_note()
        for i in range(1,len(self.notes)):
            result += self.notes[i].play_note()
        return result

ode_firstphrase = Tune([Note(('f',-2),1/2.0),Note(('a',0),1/4.0),Note(('a',0),1/4.0),
                Note(('bb',0),1/4.0), Note(('c',0),1/4.0),Note(('c',0),1/4.0),
                Note(('bb',0),1/4.0),Note(('a',0),1/4.0),Note(('g',-1),1/4.0),
                Note(('f',-1),1/4.0),Note(('f',-1),1/4.0),Note(('g',-1),1/4.0),
                Note(('a',0),1/4.0),Note(('a',0),1/4.0+1/8.0),Note(('g',-1),1/8.0),Note(('g',-1),1/2.0)])




 
if __name__ == '__main__':
    tempo = 200 #quarter note beats per minute
    ode_firstphrase.play()
    
