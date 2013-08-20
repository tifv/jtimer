from math import exp
from random import uniform

from ..core import TimerCore

class PoissonTimerCore(TimerCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remained = int(self.remained)

    def update_time(self):
        passed_time = self.time() - self.registered_time
        self.registered_time += passed_time
        self.remained -= self.poisson(passed_time)

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

