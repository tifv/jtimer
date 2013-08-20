from gi.repository import Gtk, GObject

from ..core import TimerCore

class GtkTimerCore(TimerCore):
    def __init__(self, *args, title='timer', font_size=100, **kwargs):
        super().__init__(*args, **kwargs)

        def close_handler(widget, event):
            self.close()
        def clicked_handler(widget):
            self.interact()

        self.master = Gtk.Window(title=title)
        self.label = Gtk.Label()
        self.master.connect('delete-event', close_handler)
        self.master.add(self.label)
        self.label_font_size = int(1000 * font_size)

        self.control_master = Gtk.Window(
            title=title + ' (control)',
            default_width=150, default_height=150
        )
        self.control_master.connect('delete-event', close_handler)
        self.button = Gtk.Button()
        self.button.set_label('Start/Pause')
        self.button.connect('clicked', clicked_handler)
        self.control_master.add(self.button)

        self.timeout_id = None
        self.update_label()

        self.master.show_all()
        self.control_master.show_all()

    def start(self):
        super().start()
        self.start_timeout()

    def start_timeout(self):
        assert self.timeout_id is None
        def timeout_call():
            self.update()
            return True # continue timeout
        self.timeout_id = GObject.timeout_add(25, timeout_call)

    def pause(self):
        super().pause()
        self.stop_timeout()

    def stop_timeout(self):
        assert self.timeout_id is not None
        GObject.source_remove(self.timeout_id)
        self.timeout_id = None

    def mainloop(self):
        return Gtk.main()

    def shutdown(self):
        Gtk.main_quit()

    def show_remained(self, remained):
        self.set_label_markup(self.format_remained(remained),
            colour='black' if remained > 0.0 else 'red' )

    def set_label_markup(self, label, colour='black'):
        self.label.set_markup(
            '<span font_size="{size}" foreground="{colour}">{label}</span>'
            .format(label=label, colour=colour, size=self.label_font_size) )

