import threading
import time
import logging


class Receiver:
    def __init__(self, transfer, bus):
        self.transfer = transfer
        self.bus = bus
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True
        th = threading.Thread(target=self._read_and_accept, daemon=True, args=())
        th.start()
        return th

    def _read_and_accept(self):
        """
        Reads incoming message from the transfer and adds it to currently pending data aggregation block.
        """

        last_message_seq = -1

        while self.running:

            self.transfer.wait_for_ready()
            # dont reset message sequence

            while self.running:
                msg = self.transfer.read()
                now = time.perf_counter()

                if msg is None:
                    break  # transfer signal connection reset

                # Check for packet loss
                if last_message_seq != -1:
                    seq_delta = msg.seq - last_message_seq
                    if seq_delta > 1:
                        logging.info('Packet loss detected! %d messages are absent prior to sequence %d', seq_delta, msg.seq)

                last_message_seq = msg.seq

                # Aggregate the vector, and if ready submit into event bus
                self.bus.put(ReceivedMessage(msg.payload, now))


class ReceivedMessage:
    def __init__(self, data, received_at):
        self.data = data
        self.received_at = received_at
