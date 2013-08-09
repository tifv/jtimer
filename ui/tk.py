from tkinter import Tk, Label
from functools import partial

from .common import CommonTimerApp

raise AssertionError("Tkinter version is broken.")

class TkTimerApp(CommonTimerApp):
    def __init__(self, timer, precision, title='timer'):
        super().__init__(timer, precision)

        self.master = Tk()
        self.master.wm_title(title)
        self.master.bind('<Destroy>', self.force_quit)
        self.master.bind('<KeyRelease-space>', self.space_key_release)

        self.label = Label(self.master, font='Monospace 100')
        self.label.pack(expand=True)
        self.show_remained()

        self.state = 'not started'

    def mainloop(self):
        return self.master.mainloop()

    def start_timer(self):
        self.state = 'running'
        self.timer.start_timer()
        self.show_remained(repeat=True)

    def finish_timer(self):
        self.state = 'finished'
        self.label.config(text=self.format_remained(0.0), fg='red')

    def space_key_release(self, event):
        if self.state == 'not started':
            self.start_timer()
        elif self.state == 'running':
            self.output_remained()
            self.state = 'interrupted'
            self.master.quit()
        elif self.state == 'finished':
            self.master.quit()
        return True # finish event processing

    def force_quit(self, event):
        if self.state == 'running':
            self.output_remained()
            self.state = 'interrupted'
        self.master.quit()

    def show_remained(self, repeat=False):
        remained = self.timer.remained()
        if remained <= 0:
            return self.finish_timer()
        self.label.config(text=self.format_remained(remained))
        if repeat:
            self.master.after(20, partial(self.show_remained, repeat=True))

