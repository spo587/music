import subprocess
import math
import struct
import classes_functions as cf


bit = 32
sample_rate = 5000.0
wave_peak = (2**bit - 1)/2.0
note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10,'tab':-1}



def parse_freq(note):

    half_steps_above_440 = note_dict[note]
    fund_freq = 440*2**(float(half_steps_above_440)/12)
    return fund_freq


     
def play(freq):
    ints = cf.build_sine_wave(freq,3.0,time_constant=2.0)
    bytes = cf.convert_to_bytes(ints)
    p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write(bytes)
    p.stdin.close()




if __name__ == '__main__':
    print parse_freq('c')
    play(440)
    while 1:
        play_raw_input()
    # p,bytes = play2()
    # p.stdin.write(bytes)
    # p,bytes = play2()
    # p.stdin.write(bytes)


# def play_raw_input():
#     note = str(raw_input('enter a note, plz: '))
#     freq = parse_freq(note)
#     list_of_ints = build_sine_wave(freq)
#     bytes = convert_to_bytes(list_of_ints)
#     p = subprocess.Popen(['sox', '-r', str(sample_rate), '-b', str(bit) , '-c', '1', '-t', 'raw', '-e', 'unsigned-integer', '-', '-d'], stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#     p.stdin.write(bytes)
#     p.stdin.close()
