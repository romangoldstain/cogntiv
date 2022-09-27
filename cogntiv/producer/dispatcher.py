import logging
import threading
import time
from common.message import Message


class Dispatcher:
    """
    Dispatches objects arriving though from the object bus over potentially open transfer to remote consumer.
    Dispatching tries to respect required target rate (messages per second).
    TODO:
    wait timeout
    error handling
    proper closing and thread termination
    """

    def __init__(self, transfer, monitor, bus, target_rate=1000):
        self.transfer = transfer
        self.monitor = monitor
        self.bus = bus
        self.target_rate_interval = 1.0 / target_rate
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

        unsent_msg = None

        while self.running:

            self.transfer.wait_for_ready()
            self.monitor.reset()
            # dont reset message sequence

            last_sent_at = 0

            while self.running:

                if unsent_msg is None:
                    data = self.bus.get()
                    msg = Message(self.nextMessageSeq, data)
                else:
                    msg = unsent_msg
                    unsent_msg = None

                # Upon packet loss, utilize message's time slot. Remote consumer is expected
                # to experience gap in the input stream.

                now = time.perf_counter()
                if now - last_sent_at >= self.target_rate_interval:

                    success = self.transfer.send(msg)
                    self.monitor.add_event()

                    last_sent_at = now
                else:
                    success = False

                if success:

                    self.nextMessageSeq += 1
                    if self.nextMessageSeq % 100 == 0:  # debug
                        logging.info('sent #%d at %.2f msg/sec', self.nextMessageSeq, self.monitor.get_avg_rate_per_sec())

                else:
                    unsent_msg = msg
                    if not self.transfer.is_ready():
                        break
