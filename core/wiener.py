from math import sqrt
from random import normalvariate

from .regular import RegularTimer

class WienerTimer(RegularTimer):
    # Extension
    def __init__(self, seconds):
        super().__init__(seconds)
        self.duration = sqrt(self.duration)

    # Extension
    def remained(self):
        remained = super().remained()
        if remained > 0.0:
            return remained**2
        else:
            return remained

    # Override
    def update_running(self):
        passed_time = self.time() - self.current_time
        self.current_time += passed_time
        self.duration -= self.wiener(passed_time)

    @staticmethod
    def wiener(passed_time):
        return normalvariate(0, 1.4826022184455 * sqrt(passed_time))

