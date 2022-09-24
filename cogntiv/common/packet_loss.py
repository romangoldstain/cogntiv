import time
from abc import ABC, abstractmethod
import numpy as np


class LossPolicy(ABC):
    @abstractmethod
    def should_loose(self):
        pass

    @staticmethod
    def never():
        return Never()

    @staticmethod
    def within_interval(lower, upper):
        return OneWithinInterval(lower, upper)


class Never(LossPolicy, ABC):
    def should_loose(self):
        return False


class OneWithinInterval(LossPolicy, ABC):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.anchor_time = time.perf_counter()

    def should_loose(self):
        now = time.perf_counter()
        delta = now - self.anchor_time

        if delta > self.upper:
            self.anchor_time = time.perf_counter()
            return False

        if delta >= self.lower:
            drop = np.random.uniform() > 0.5  # uniform() returns random([0,1)) -> false = [0, 0.5) ; true = [0.5, 1)
            if drop:
                self.anchor_time = time.perf_counter()
            return drop

        return False
