import math


class StatsHelper:
    def __init__(self):
        self._count = 0
        self._mean = 0
        self._var = 0
        self._std = 0

    def add_value(self, value):
        self._mean = (self._count * self._mean + value) / (self._count + 1)
        if self._count > 0:
            self._var = ((self._count + 1) / self._count) * (
                        ((self._count * self._var) / (self._count + 1)) + (((value - self._mean) ** 2) / self._count))

        self._std = math.sqrt(self._var)
        self._count += 1

    def mean(self):
        return self._mean

    def std(self):
        return self._std
