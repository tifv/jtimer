from gi.repository import Gtk, GObject

from .common import CommonTimerApp

class GtkTimerApp(CommonTimerApp):
    def __init__(self, timer, precision, title='timer'):
        super().__init__(timer, precision)

        self.master = Gtk.Window(title=title)
        self.master.connect('delete-event', self.force_quit)
        self.master.connect('key-release-event', self.key_release)

        self.label = Gtk.Label()
        self.master.add(self.label)
        self.show_remained()

        self.state = 'not started'
        self.master.show_all()

    def mainloop(self):
        return Gtk.main()

    def start_timer(self):
        self.state = 'running'
        self.timer.start_timer()
        GObject.timeout_add(
            20, lambda userdata: self.show_remained(), None )

    def finish_timer(self):
        self.state = 'finished'
        self.set_markup(self.format_remained(0.0), colour='red')

    def key_release(self, widget, event):
        if event.keyval == 32:
            return self.space_key_release(widget, event)

    def space_key_release(self, widget, event):
        if self.state == 'not started':
            self.start_timer()
        elif self.state == 'running':
            self.output_remained()
            Gtk.main_quit()
        elif self.state == 'finished':
            Gtk.main_quit()
        return True # finish event processing

    def force_quit(self, widget, event):
        if self.state == 'running':
            self.output_remained()
        Gtk.main_quit()

    def show_remained(self):
        remained = self.timer.remained()
        if remained <= 0:
            self.finish_timer()
            return False # stop timer
        self.set_markup(self.format_remained(remained))
        return True # continue timer

    def set_markup(self, label, colour='black'):
        self.label.set_markup(
            '<span font_size="100000" foreground="{colour}">{label}</span>'
            .format(label=label, colour=colour) )

