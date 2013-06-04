import time

class RegularTimer:
    def __init__(self, seconds):
        self.start_time = None
        self.current_time = None
        self.duration = seconds

    def time(self):
        return time.time()

    def start_timer(self):
        self.start_time = self.time()

    def remained(self):
        if self.start_time is None:
            return self.duration
        return self.duration + self.start_time - self.time()

