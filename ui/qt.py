from PyQt4 import QtGui, QtCore

from ..core import TimerCore

class QtTimerCore(TimerCore):
    def __init__(self, *args, title='timer', font_size=100, **kwargs):
        super().__init__(*args, **kwargs)

        self.qapp = QtGui.QApplication([])

        self.master = MasterWindow()
        self.master.setWindowTitle(title)
        self.master.close_callback = self.close
        self.label = QtGui.QLabel('', self.master)

        label_font = QtGui.QFont()
        label_font.setPointSize(font_size)
        self.label.setFont(label_font)

        master_layout = QtGui.QGridLayout(self.master)
        master_layout.addWidget(self.label)
        master_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.master.setLayout(master_layout)

        self.control = ControlWindow()
        self.control.setWindowTitle(title + ' (control)')
        self.control.resize(150, 150)
        self.control.close_callback = self.close
        self.button = QtGui.QPushButton('Start/Pause', self.control)
        self.button.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
        self.button.clicked.connect(self.interact)

        control_layout = QtGui.QGridLayout(self.control)
        control_layout.addWidget(self.button)
        self.control.setLayout(control_layout)

        self.master.timer_callback = self.update
        self.update_label()

        self.master.show()
        self.control.show()

    def start(self):
        super().start()
        self.start_timeout()

    def start_timeout(self):
        self.timer_id = self.master.startTimer(25)

    def pause(self):
        super().pause()
        self.stop_timeout()

    def stop_timeout(self):
        self.master.killTimer(self.timer_id)

    def mainloop(self):
        return self.qapp.exec()

    def shutdown(self):
        return self.qapp.quit()

    def show_remained(self, remained):
        self.label.setText(self.format_remained(remained))
        if remained > 0.0:
            pass
        else:
            self.label.setStyleSheet('QLabel { color : red; }')

class Window(QtGui.QWidget):
    close_callback = None

    def closeEvent(self, event):
        assert self.close_callback is not None
        self.close_callback()
        super().closeEvent(event)

class MasterWindow(Window):
    timer_callback = None

    def timerEvent(self, event):
        assert self.timer_callback is not None
        self.timer_callback()
        super().timerEvent(event)

class ControlWindow(Window):
    pass

