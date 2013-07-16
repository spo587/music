import subprocess
import classes_functions as msw 
import time
from collections import defaultdict




def make_instrument(name,dict1,dict2,dict3,dict4):
    return msw.Instrument(name,dict3,dict1,dict2,dict4)

def make_crappy_instrument():

    dict1 = {1:0.5, 2: 0.1, 3: 0.1, 4: 0.05, 5: 0.05, 6: 0.01, 7:0.01, 8: 0.01, 9: 0.01}
    dict2 = {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.2, 5: 7.0, 6: 12.0, 7: 12.0, 8:7.0, 9: 8.0}
    dict3 = {}
    for i in range(1,5):
        dict3[i] = msw.linear_decay
    for i in range(5,14):
        dict3[i] = msw.exponential_decay
    dict4 = {}
    for i in range(1,10):
        dict4[i] = 0.01
    return dict1,dict2,dict3,dict4

dict1,dict2,dict3,dict4 = make_crappy_instrument()


crappy_instrument = make_instrument('crappy',dict1,dict2,dict3,dict4)


def make_second_instrument():
    dict5 = {1:0.7,2:0.5,3:0.3,4:0.2}
    dict6 = {1:1.2,2:1.5,3:1.0,4:1.0}
    dict7 = {}
    for i in range(1,5):
        dict7[i] = msw.linear_decay
    # dict7[3] = msw.exponential_decay
    # dict7[4] = msw.exponential_decay
    dict8 = {}
    for i in range(1,5):
        dict8[i] = 0.0
    return dict5,dict6,dict7,dict8

dict5,dict6,dict7,dict8 = make_second_instrument()

second_instrument = make_instrument('second',dict5,dict6,dict7,dict8)

 
def twinkle_twinkle():

    a = msw.Tone('a',0,1.0,crappy_instrument)
    e = msw.Tone('e',0,1.0,crappy_instrument)
    fsharp = msw.Tone('f#',0,1.0,crappy_instrument)
    d = msw.Tone('d',0,1.0,crappy_instrument)
    csharp = msw.Tone('c#',0,1.0,crappy_instrument)
    csharp_16th = msw.Tone('c#',0,1/4.0,crappy_instrument) 
    b = msw.Tone('b',0,3/4.0,crappy_instrument)
    a_whole = msw.Tone('a',0,2.0,crappy_instrument)
    bass_a = msw.Tone('a',-2,1.0,crappy_instrument)
    middle_a = msw.Tone('a',-1,1.0,crappy_instrument)
    bass_csharp = msw.Tone('c#',-1,1.0,crappy_instrument)
    middle_d = msw.Tone('d',-1,1.0,crappy_instrument)
    bass_b = msw.Tone('b',-1,1.0,crappy_instrument)
    bass_gsharp = msw.Tone('g#',-2,1.0,crappy_instrument)
    bass_fsharp = msw.Tone('f#',-2,1.0,crappy_instrument)
    bass_d = msw.Tone('d',-2,1.0,crappy_instrument)
    bass_e = msw.Tone('e',-2,1.0,crappy_instrument)
    bass_a_whole = msw.Tone('a',-2,4.0,crappy_instrument)
    a_16th = msw.Tone('a',0,1/16.0,crappy_instrument)

    melody = [a,a,e,e,fsharp,fsharp,e,e,
              d,d,csharp,csharp,b,a_16th,b,csharp_16th,a_whole]
    bass = [bass_a,middle_a,bass_csharp,middle_a,middle_d,
            middle_a,bass_csharp,middle_a,bass_b,bass_gsharp,middle_a,
            bass_fsharp,bass_d,bass_e,bass_a_whole]

    
    melody1 = msw.combine_things_ints(melody)
    
    bassline = msw.combine_things_ints(bass)
    chords = msw.combine_n_waves(melody1,bassline)

    # melody_bass = zip(melody,bass)

    # chords = [Chord(item) for item in melody_bass]
    return chords

def somewhere1():
    one = msw.Tone('a',-1,2.0,crappy_instrument)
    two = msw.Tone('a',-0,2.0,crappy_instrument)
    three = msw.Tone('g#',-1,1.0,crappy_instrument)
    four = msw.Tone('e',-1,1/2.0,crappy_instrument)
    five = msw.Tone('f#',-1,1/2.0,crappy_instrument)
    six = three
    seven = msw.Tone('a',-0,1.0,crappy_instrument)
    eight = msw.Tone('f#',-2,2.0,crappy_instrument)
    nine = msw.Tone('f#',-1,2.0,crappy_instrument)
    ten = msw.Tone('e',-1,4.0,crappy_instrument)
    offset_bass = msw.Tone('rest',None,8.0,crappy_instrument)

    offset = msw.Tone('rest',None,8.0,crappy_instrument)
    one_bass = msw.Tone('a',0,2.0,crappy_instrument)
    two_bass = msw.Tone('a',1,2.0,crappy_instrument)
    three_bass = msw.Tone('g#',0,1.0,crappy_instrument)
    four_bass = msw.Tone('e',0,1/2.0,crappy_instrument)
    five_bass = msw.Tone('f#',0,1/2.0,crappy_instrument)
    six_bass = three_bass
    seven_bass = msw.Tone('a',1,1.0,crappy_instrument)
    eight_bass = msw.Tone('f#',-1,2.0,crappy_instrument)
    nine_bass = msw.Tone('f#',0,2.0,crappy_instrument)
    ten_bass = msw.Tone('e',0,1.0,crappy_instrument)
    melody_bass = [one,two,three,four,five,six,seven,eight,nine,ten,offset_bass]
    melody_treble = [offset,one_bass,two_bass,three_bass,four_bass,five_bass,six_bass,seven_bass,eight_bass,nine_bass,ten_bass]

    bassline = msw.combine_things_ints(melody_bass)
    treble_line = msw.combine_things_ints(melody_treble)
    chords = msw.combine_n_waves(treble_line,bassline)

    return chords


def somewhere2():
    line1 = msw.Line([['eb',-1,2.0],['eb',0,2.0],['d',0,1.0],['bb',0,1/2.0],['c',0,1/2.0],['d',0,1.0],
                    ['eb',0,1.0],['eb',-1,2.0],['c',0,2.0],['bb',0,4.0],
                    ['c',-1,2.0],['ab',-0,2.0],['g',-1,1.0],['eb',-1,1/2.0],['f',-1,1/2.0],
                    ['g',-1,1.0],['ab',-0,1.0],['f',-1,1.0],['d',-1,0.5],['eb',-1,0.5],['f',-1,1.0],
                    ['g',-1,1.0],['eb',-1,4.0]],crappy_instrument)
    line2 = msw.Line([['bb',-1,2.0],['bb',0,2.0],['f',-1,3.0],['g',-1,1.0],['eb',-1,4.0],['eb',-1,4.0],
                    ['c',-1,3.0],['d',-1,0.5],['c',-1,0.5],['b',-1,2.0],['c',-1,2.0],['rest',None,1.5],['eb',-1,1.5],
                    ['d',-1,1.0],['eb',-1,4.0]],crappy_instrument)
    line3 = msw.Line([['g',-2,2.0],['g',-1,2.0],['rest',None,4.0],['c',-1,1.0],['ab',-1,0.5],['bb',-1,0.5],
                    ['c',-1,1.0],['d',-1,1.0],['eb',-1,4.0],['rest',None,6.0],['bb',-1,2.0],['c',-1,3.0],
                    ['bb',-1,1.0],['g',-2,4.0]],second_instrument)

    line4 = msw.Line([['rest',None, 4.0],['bb',-2,2.0],['bb',-1,2.0],['rest',None,1.0],['ab',-1,3.0],
                    ['g',-2,1.0],['eb',-2,0.5],['f',-2,0.5],['g',-2,1.0],['ab',-1,1/2.0],['bb',-1,0.5],
                    ['ab',-1,2.0],['f',-3,2.0],['g',-3,1.0],['f',-2,1.0],['e',-2,1.0],
                    ['f',-2,0.5],['g',-2,0.5],['ab',-1,1.5],['g',-2,0.5],['ab',-1,0.5],
                    ['a',-1,0.5],['bb',-1,1.0],['eb',-2,4.0]],second_instrument)

    lines = [line1,line2,line3,line4]

    lines_ready = [msw.combine_things_ints(line.make_tones()) for line in lines]

    chords = msw.combine_n_waves(lines_ready[0],lines_ready[1],lines_ready[2],lines_ready[3])
    return chords

def somewhere3():
    line1 = msw.Line_steps([[1,2,2.0],[1,3,2.0]],crappy_instrument)
    print line1.notes_value_pairs

    line2 = msw.Line_steps([[5,1,2.0],[5,2,2.0]],crappy_instrument)

    line3 = msw.Line_steps([[3,1,2.0],['rest',2,2.0]],crappy_instrument)

    lines = [line1]#, line2,line3]
    lines_ready = [msw.combine_things_ints(line.make_tones()) for line in lines]
    chords = msw.combine_n_waves(lines_ready[0])#,lines_ready[1],lines_ready[2])
    return chords

def input_tune_quarter_notes():
    instrument = crappy_instrument
    steps = (raw_input('input the scale degrees in a list'))
    list_notes = [[int(step),2,1.0] for step in steps]
    line1 = msw.Line_steps(list_notes,instrument)
    print line1.notes_value_pairs
    lines_ready = [msw.combine_things_ints(line1.make_tones())]
    chords = msw.combine_n_waves(lines_ready[0])
    return chords


if __name__ == '__main__':
    # t_0 = time.time()
    # #tune1 = bach_herzliebster()
    tune1 = somewhere2()
    # t_1 = time.time()
    # print t_1 - t_0
    #msw.write_to_file(tune1,'ohshit')
    msw.play2(tune1)
    #tune1 = input_tune_quarter_notes()
    #msw.play2(tune1)
    



def bach_herzliebster():

    soprano = msw.Line([['a',0,1.0],['a',-0,1.0],['a',-0,1.0],['g#',-1,1/2.0],['f#',-1,1/2.0],
                        ['e',-1,1.0]],crappy_instrument) 

    alto = msw.Line([['e',-1,1.0],['f',-1,1.0],['f',-1,1.0],['e',-1,1.0],['b',-1,1.0]],crappy_instrument)
    
    tenor = msw.Line([['c',-1,1.0],['d',-1,1.0],['c',-1,1.0],['b',-1,1/2.0],['a',-1,1/2.0],
                    ['g#',-2,1.0]],crappy_instrument)

    bass = msw.Line([['a',-1,1.0],['d',-2,1/2.0],['e',-2,1/2.0],['f',-2,1/2.0],['d',-2,1/2.0],
                    ['e',-2,3/2.0],['d',-2,1/2.0]],crappy_instrument)

    lines = [soprano,alto,tenor,bass]
    lines_ready = [msw.combine_things_ints(line.make_tones()) for line in lines]

    chords = msw.combine_n_waves(lines_ready[0],lines_ready[1],lines_ready[2],lines_ready[3])
    return chords
    
    
