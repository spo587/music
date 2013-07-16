import urwid
import test


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        if key in test.note_dict.keys():
            return test.play(test.parse_freq(key))


edit = urwid.Edit(u"enter notes to play\n")
fill = QuestionBox(edit)
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()