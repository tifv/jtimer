from math import exp
from random import uniform

from .regular import RegularTimer

class PoissonTimer(RegularTimer):
    # Extension
    def __init__(self, seconds):
        super().__init__(seconds)
        self.duration = int(self.duration)

    # Override
    def update_running(self):
        passed_time = self.time() - self.current_time
        self.current_time += passed_time
        self.duration -= self.poisson(passed_time)

    @staticmethod
    def poisson(mean):
        x = uniform(0, 1)
        k = 0
        p = exp(-mean)
        while (x > p):
            x -= p
            k += 1
            p *= mean / k
        else:
            return k

