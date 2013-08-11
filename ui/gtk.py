from gi.repository import Gtk, GObject

from .common import CommonTimerApp

class GtkTimerApp(CommonTimerApp):
    def __init__(self, timer, precision, title='timer', font_size=100):
        super().__init__(timer, precision)

        self.master = Gtk.Window(title=title)
        self.label = Gtk.Label()
        self.master.connect('delete-event', self.force_quit)
        self.master.add(self.label)
        self.label_font_size = int(1000 * font_size)

        self.control_master = Gtk.Window(
            title=title+' (control)',
            default_width=150, default_height=150
        )
        self.control_master.connect('delete-event', self.force_quit)
        self.button = Gtk.Button()
        self.button.set_label("Start/Pause")
        def clicked_handler(widget):
            self.interact()
        self.button.connect('clicked', clicked_handler)
        self.control_master.add(self.button)

        self.redundant_timeout = 0
        self.update_timer()

        self.master.show_all()
        self.control_master.show_all()

    def mainloop(self):
        return Gtk.main()

    def interact(self):
        if self.living:
            self.toggle_timer()
        else:
            Gtk.main_quit()

    def toggle_timer(self):
        self.timer.toggle_timer()
        if self.timer.running:
            GObject.timeout_add(
                20, lambda userdata: self.update_timer(), None )
        else:
            self.redundant_timeout += 1

    def force_quit(self, widget, event):
        if self.living:
            self.output_remained()
        Gtk.main_quit()

    def update_timer(self):
        self.show_remained(self.remained())
        if not self.living:
            self.finish_timer()
            self.redundant_timeout += 1
        if self.redundant_timeout > 0:
            self.redundant_timeout -= 1
            return False # break timeout
        return True # continue timeout

    def show_remained(self, remained):
        self.set_markup(self.format_remained(remained))

    def finish_timer(self):
        self.set_markup(self.format_remained(0.0), colour='red')

    def set_markup(self, label, colour='black'):
        self.label.set_markup(
            '<span font_size="{size}" foreground="{colour}">{label}</span>'
            .format(label=label, colour=colour, size=self.label_font_size) )

