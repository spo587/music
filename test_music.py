import subprocess
import os


#g_rate = 60000 
class Note(object):
    tempo = 200
    note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10}
    for note in note_dict.keys():
        note_dict[note + '#'] = note_dict[note] + 1
        note_dict[note + 'b'] = note_dict[note] - 1
        #doublesharps and flats too

    def __init__(self, name, value):
        '''name a tuple of (note name, octave)'''
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
        self.notes = notes
    def play(self):
        result = notes[0].play_note()
        for i in range(1,len(self.notes)):
            result += notes[i].play_note()
        return result

ode_firstphrase = Tune([Note(('f',-2),1/2.0),Note(('a',0),1/4.0),Note(('bb',0),1/4.0),Note(('a',0),1/4.0)])
note1 = Note(('b#',0),2.0)



def play_tune(half_steps_above_440_and_length_list):
    result = play_waveform(make_note_simpler(half_steps_above_440_and_length_list[0]))
    for i in range(1,len(half_steps_above_440_and_length_list)):
        result += play_waveform(make_note_simpler(half_steps_above_440_and_length_list[i]))
    return result



        
 
# def play(*notes):
#     play_waveform(''.join([n.get_waveform(8000) for n in notes]))
 
if __name__ == '__main__':
    tempo = 300
    note1.play_note()
    
    #for i in range(-2,4):
    #    play_waveform(make_note(g_rate,i,.5))