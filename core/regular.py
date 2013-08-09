import time

class RegularTimer:
    def __init__(self, seconds):
        self.current_time = None
        self.duration = seconds
        self.running = False

    def time(self):
        return time.time()

    def toggle_timer(self, running=None):
        if not self.running:
            if running is False:
                return
            self.start_timer()
            self.running = True
        else:
            if running is True:
                return
            self.pause_timer()
            self.running = False

    def start_timer(self):
        self.current_time = self.time()

    def pause_timer(self):
        self.update_running()
        self.current_time = None

    def update_running(self):
        passed_time = self.time() - self.current_time
        self.current_time += passed_time
        self.duration -= passed_time

    def remained(self):
        if self.running:
            self.update_running()
        return self.duration

