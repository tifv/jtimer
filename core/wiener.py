from math import sqrt
from random import normalvariate

from .regular import RegularTimer

class WienerTimer(RegularTimer):
    def __init__(self, seconds):
        self.wiener_last = None
        super().__init__(seconds)
        self.original_duration = self.duration
        self.duration = sqrt(self.duration)

    def start_timer(self):
        super().start_timer()
        self.wiener_last = self.start_time

    def remained(self):
        if self.wiener_last is None:
            return self.original_duration
        time_passed = self.time() - self.wiener_last
        self.wiener_last += time_passed
        self.duration -= self.wiener(time_passed)
        return self.duration**2 if self.duration >= 0.0 else self.duration

    @staticmethod
    def wiener(time_passed):
        return normalvariate(0, 1.4826022184455 * sqrt(time_passed))

