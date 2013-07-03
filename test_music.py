import subprocess
import os

g_rate = 60000 
def play_waveform(form):
    s = '%s | play -n synth 1 sine' %form
    #s = 'echo %s | sox -r 60000 -b 8 -c 1 -t raw -s - -d' % form
    #print s
    os.system(s)
 
    #p = subprocess.Popen(['sox', '-r', '8000', '-b', '8', '-c', '1', '-t', 'raw', '-s', '-', '-d'], stdin=subprocess.PIPE)
    #p.stdin.write(form)
    
 
def make_note(rate, half_steps_above_400, length=1):
    cycles = int(rate / (400 * 2**(float(half_steps_above_400)/12)))
    cycle = cycles/2 * 'a' + cycles/2 * 'r'
    return int(rate / len(cycle) * length) * cycle
 
 
class Note(object):
    def __init__(self, half_steps_above_440, dur):
        pass
    def get_waveform():
        pass
 
def play(*notes):
    play_waveform(''.join([n.get_waveform(8000) for n in notes]))
 
if __name__ == '__main__':
    #play_waveform(make_note(g_rate, 0, .5) + make_note(g_rate, 0, .5) +  make_note(g_rate, 1, .5) + make_note(g_rate, 3, .5))
    play_waveform(490)

    #for i in range(-2,4):
    #    play_waveform(make_note(g_rate,i,.5))