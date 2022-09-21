import threading
import time
from common.message import Message


class Dispatcher:

    def __init__(self, transfer, vector_bus):
        self.transfer = transfer
        self.vector_bus = vector_bus
        self.running = False
        self.nextMessageSeq = 1
        # stats
        self.sentCount = 0
        self.totalDurationInSec = 0

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
            start_time = time.perf_counter()

            while self.running:

                if unsent is None:
                    vector = self.vector_bus.get()
                    msg = Message(self.nextMessageSeq, vector)
                else:
                    msg = unsent
                    unsent = None

                success = self.transfer.send(msg)
                if success:

                    now = time.perf_counter()

                    self.nextMessageSeq += 1

                    # update stats
                    self.sentCount += 1
                    self.totalDurationInSec = now - start_time

                    if self.sentCount % 5 == 0:
                        print(f"sent #{self.nextMessageSeq} at {self.sentCount / self.totalDurationInSec} msg/sec")

                else:
                    unsent = msg
                    if not self.transfer.is_ready():
                        break

                self.vector_bus.task_done()  # The vector is out of the bus any way
                time.sleep(1)


"""
retry
wait timeout
"""
