import time


class RateMonitor:

    def __init__(self):
        self.start_time = time.perf_counter()
        self.event_count = 0

    def reset(self):
        self.start_time = time.perf_counter()
        self.event_count = 0
        pass

    def add_event(self, count=1):
        self.event_count += count

    def get_avg_rate_per_sec(self):
        now = time.perf_counter()
        return self.event_count / (now - self.start_time)
