import time
from abc import ABC, abstractmethod
import numpy as np


class LossPolicy(ABC):
    """
    Defines the policy according which packets (message) loss is happening.
    """

    @abstractmethod
    def should_loose(self):
        """
        Indicates whether the upcoming message should be dropped (lost) or not.
        """
        pass

    @staticmethod
    def never():
        return Never()

    @staticmethod
    def within_interval(lower, upper):
        return OneWithinInterval(lower, upper)


class Never(LossPolicy):
    def should_loose(self):
        return False


class OneWithinInterval(LossPolicy):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.anchor_time = time.perf_counter()

    def should_loose(self):
        now = time.perf_counter()
        delta = now - self.anchor_time

        if delta > self.upper:
            self.anchor_time = now
            return False

        if delta >= self.lower:
            drop = np.random.uniform() > 0.5  # uniform() returns random([0,1)) -> false = [0, 0.5) ; true = [0.5, 1)
            if drop:
                self.anchor_time = now
            return drop

        return False
