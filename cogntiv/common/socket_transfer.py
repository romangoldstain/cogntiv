import time
from multiprocessing.connection import Listener
from multiprocessing.connection import Client


class SocketTransfer:

    def __init__(self, address, port, loss_policy):
        self.listener = Listener((address, port))
        self.loss_policy = loss_policy
        self.conn = None
        self.isClosed = False
        self.connected_at = None
        self.loss_count = 0

    def wait_for_ready(self):

        print("Waiting for connection...")

        try:
            self.conn = self.listener.accept()
            self.connected_at = time.perf_counter()
            print('Connection accepted from', self.listener.last_accepted)
        except OSError:
            if not self.isClosed:
                print("Exception while accepting new connection")
                self.listener.close()
            # else - that's fine, the transfer was explicitly closed.

    def close(self):
        if not self.isClosed:
            self.isClosed = True
            self.listener.close()  # can throw?

    def send(self, message):
        if self.conn is None:
            raise RuntimeError("Connection was not established.")

        if self.loss_policy.should_loose():
            self.loss_count += 1
            print(f'Packet loss :( so far - {self.loss_count} messages lost')
            return True

        try:
            self.conn.send(message)
            return True
        except ConnectionError:
            print("Connection broken :(")
            self.conn = None
            return False

    def is_ready(self):
        return self.conn is not None


class SocketTransferClient:

    def __init__(self, address, port):
        self.address = (address, port)
        self.conn = None
        self.isClosed = False
        self.connected_at = None
        self.loss_count = 0

    def wait_for_ready(self):

        print("Connecting...")

        try:
            self.conn = Client(self.address)
            self.connected_at = time.perf_counter()
            print('Connection established.')
        except OSError:
            if not self.isClosed:
                print("Exception while accepting new connection")
            # else - that's fine, the transfer was explicitly closed.

    def close(self):
        if not self.isClosed:
            self.isClosed = True
            self.conn.close()  # can throw?

    def read(self):
        if self.conn is None:
            raise RuntimeError("Connection was not established.")

        try:
            return self.conn.recv()
        except ConnectionResetError:
            print("Connection broken :(")
            self.conn = None
            return None

    def is_ready(self):
        return self.conn is not None
