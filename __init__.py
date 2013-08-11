def main(minutes, precision=0, flavour='regular', ui='gtk', immediate=False, font_size=100):
    seconds = minutes * 60
    if flavour == 'regular':
        from .core.regular import RegularTimer as Timer
        title = 'Regular timer'
    elif flavour == 'poisson':
        from .core.poisson import PoissonTimer as Timer
        title = 'Poisson timer'
    elif flavour == 'wiener':
        from .core.wiener import WienerTimer as Timer
        title = 'Wiener timer'
    else:
        raise ValueError(flavour)
    if ui == 'tk':
        from .ui.tk import TkTimerApp as TimerApp
    elif ui == 'gtk':
        from .ui.gtk import GtkTimerApp as TimerApp
    else:
        raise ValueError(ui)
    app = TimerApp(Timer(seconds), precision, title=title, font_size=font_size)
    if immediate:
        app.toggle_timer()
    app.mainloop()

def set_terminal_caption(caption=None):
    import sys
    if caption is None:
        caption = sys.argv[0].rpartition('/')[2]
    sys.stdout.write('\033]2;' + caption + '\007')
    sys.stdout.flush()

