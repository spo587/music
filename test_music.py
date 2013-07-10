import subprocess
import make_sine_wave as msw 
import time


 
def twinkle_twinkle():

    a = msw.Tone(('a',0),1/4.0)
    e = msw.Tone(('e',0),1/4.0)
    fsharp = msw.Tone(('f#',0),1/4.0)
    d = msw.Tone(('d',0),1/4.0)
    csharp = msw.Tone(('c#',0),1/4.0)
    csharp_16th = msw.Tone(('c#',0),1/16.0) 
    b = msw.Tone(('b',0),3/16.0)
    a_whole = msw.Tone(('a',0),1.0/2.0)
    bass_a = msw.Tone(('a',-2),1.0/4.0)
    middle_a = msw.Tone(('a',-1),1.0/4.0)
    bass_csharp = msw.Tone(('c#',-1),1/4.0)
    middle_d = msw.Tone(('d',-1),1/4.0)
    bass_b = msw.Tone(('b',-1),1/4.0)
    bass_gsharp = msw.Tone(('g#',-2),1/4.0)
    bass_fsharp = msw.Tone(('f#',-2),1/4.0)
    bass_d = msw.Tone(('d',-2),1/4.0)
    bass_e = msw.Tone(('e',-2),1/4.0)
    bass_a_whole = msw.Tone(('a',-2),1/2.0)
    a_16th = msw.Tone(('a',0),1/16.0)

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

def somewhere():
    one = msw.Tone(('a',-1),1/2.0)
    two = msw.Tone(('a',-0),1/2.0)
    three = msw.Tone(('g#',-1),1/4.0)
    four = msw.Tone(('e',-1),1/8.0)
    five = msw.Tone(('f#',-1),1/8.0)
    six = three
    seven = msw.Tone(('a',-0),1/4.0)
    eight = msw.Tone(('f#',-2),1/2.0)
    nine = msw.Tone(('f#',-1),1/2.0)
    ten = msw.Tone(('e',-1),1.0)
    offset_bass = msw.Tone(('a',1),2.0,instrument=silence)

    offset = msw.Tone(('a',1),2.0,instrument=silence)
    one_bass = msw.Tone(('a',0),1/2.0)
    two_bass = msw.Tone(('a',1),1/2.0)
    three_bass = msw.Tone(('g#',0),1/4.0)
    four_bass = msw.Tone(('e',0),1/8.0)
    five_bass = msw.Tone(('f#',0),1/8.0)
    six_bass = three_bass
    seven_bass = msw.Tone(('a',1),1/4.0)
    eight_bass = msw.Tone(('f#',-1),1/2.0)
    nine_bass = msw.Tone(('f#',0),1/2.0)
    ten_bass = msw.Tone(('e',0),1.0)
    melody_bass = [one,two,three,four,five,six,seven,eight,nine,ten,offset_bass]
    melody_treble = [offset,one_bass,two_bass,three_bass,four_bass,five_bass,six_bass,seven_bass,eight_bass,nine_bass,ten_bass]

    bassline = msw.combine_things_ints(melody_bass)
    treble_line = msw.combine_things_ints(melody_treble)
    chords = msw.combine_n_waves(treble_line,bassline)

    return chords

def bach_herzliebster():

    soprano = msw.Line([[('a',0),1/4.0],[('a',-0),1.0/4.0],[('a',-0),1.0/4.0],[('g#',-1),1.0/4.0],
                        [('e',-1),1/4.0]],msw.crappy_instrument) 

    alto = msw.Line([[('e',-1),1/4.0],[('f',-1),1/4.0],[('f',-1),1/4.0],[('e',-1),1/4.0],[('b',-1),1/4.0]],msw.crappy_instrument)
    
    tenor = msw.Line([[('c',-1),1/4.0],[('d',-1),1/4.0],[('c',-1),1/4.0],[('b',-1),1/8.0],[('a',-1),1/8.0],[('g#',-2),1/4.0]],msw.crappy_instrument)

    bass = msw.Line([[('a',-1),1.0/4.0],[('d',-2),1.0/8.0],[('e',-2),1.0/8.0],[('f',-2),1.0/8.0],[('d',-2),1.0/8.0],[('e',-2),3.0/8.0],
                    [('d',-2),1.0/8.0]],msw.crappy_instrument)

    lines = [soprano,alto,tenor,bass]
    lines_ready = [msw.combine_things_ints(line.make_tones()) for line in lines]

    chords = msw.combine_n_waves(lines_ready[0],lines_ready[1],lines_ready[2],lines_ready[3])
    return chords

if __name__ == '__main__':
    t_0 = time.time()
    tune1 = bach_herzliebster()
    t_1 = time.time()
    print t_1 - t_0
    msw.play2(tune1)
    


    
    
