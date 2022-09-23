import threading
import time
from common.message import Message


class Dispatcher:

    def __init__(self, transfer, monitor, bus):
        self.transfer = transfer
        self.monitor = monitor
        self.bus = bus
        self.running = False
        self.nextMessageSeq = 1

    def start(self):
        if self.running:
            return

        self.running = True
        th = threading.Thread(target=self._poll_and_dispatch, daemon=True, args=())
        th.start()
        return th

    def stop(self):
        self.running = False
        self.transfer.close()  # will interrupt any socket accept waits

    def _poll_and_dispatch(self):

        unsent = None

        while self.running:

            self.transfer.wait_for_ready()
            self.monitor.reset()

            last_sent_at = 0

            while self.running:

                if unsent is None:
                    data = self.bus.get()
                    msg = Message(self.nextMessageSeq, data)
                else:
                    msg = unsent
                    unsent = None

                now = time.perf_counter()
                if now - last_sent_at >= 0.001:
                    success = self.transfer.send(msg)
                    self.monitor.add_event()

                    last_sent_at = now
                else:
                    success = False

                if success:

                    self.nextMessageSeq += 1
                    if self.nextMessageSeq % 5 == 0:
                        print(f"sent #{self.nextMessageSeq} at {self.monitor.get_avg_rate_per_sec()} msg/sec")

                else:
                    unsent = msg
                    if not self.transfer.is_ready():
                        break

                # self.bus.task_done()  # The vector is out of the bus any way
                # time.sleep(0.2)


"""
retry
wait timeout
"""
