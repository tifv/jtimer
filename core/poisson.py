from math import exp
from random import uniform

from .regular import RegularTimer

class PoissonTimer(RegularTimer):
    def __init__(self, seconds):
        self.poisson_last = None
        super().__init__(seconds)
        self.duration = int(self.duration)

    def start_timer(self):
        super().start_timer()
        self.poisson_last = self.start_time
        self.duration -= 1

    def remained(self):
        if self.poisson_last is None:
            return self.duration
        time_passed = self.time() - self.poisson_last
        self.poisson_last += time_passed
        self.duration -= self.poisson(time_passed)
        return self.duration

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

