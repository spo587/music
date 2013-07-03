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


def play_waveform((length, freq)):
    s = 'play -n synth %s sine %s' % (length, freq)
    #s = 'echo %s | sox -r 60000 -b 8 -c 1 -t raw -s - -d' %form
    #print s
    return os.system(s)
 
    #p = subprocess.Popen(['sox', '-r', '8000', '-b', '8', '-c', '1', '-t', 'raw', '-s', '-', '-d'], stdin=subprocess.PIPE)
    #p.stdin.write(form)
    
 
def make_note(rate, half_steps_above_400, length=1):
    cycles = int(rate / (400 * 2**(float(half_steps_above_400)/12)))
    cycle = cycles/2 * 'a' + cycles/2 * 'r'
    return int(rate / len(cycle) * length) * cycle


def length(note_value):
    '''tempo in beats per minute'''
    return note_value*4*60/float(tempo)

def make_note_simpler((half_steps_above_440, note_value)):
    freq = 440*2**(float(half_steps_above_440)/12)
    return (length(note_value),freq)
 
 

        
 
# def play(*notes):
#     play_waveform(''.join([n.get_waveform(8000) for n in notes]))
 
if __name__ == '__main__':
    tempo = 300
    note1.play_note()
    #play_waveform(make_note(g_rate, 0, .5) + make_note(g_rate, 0, .5) +  make_note(g_rate, 1, .5) + make_note(g_rate, 3, .5))
    play_tune([(0,0.5),(0,0.5),(1,0.5),(3,0.5),(3,0.5),(1,0.5),(0,0.5),(-2,0.5),(-4,0.5),(-4,0.5),(-2,0.5),(0,0.5),(0,0.75),(-2,0.25),(-2,0.5)])
    #play_waveform(make_note_simpler(0,0.01)) #+ play_waveform(make_note_simpler(0)) + play_waveform(make_note_simpler(1)) + play_waveform(make_note_simpler(3))

    #for i in range(-2,4):
    #    play_waveform(make_note(g_rate,i,.5))