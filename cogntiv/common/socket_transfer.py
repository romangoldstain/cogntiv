from multiprocessing.connection import Listener


class SocketTransfer:

    def __init__(self, address, port):
        self.conn = None
        self.listener = None
        self.isClosed = False
        self.listener = Listener((address, port))

    def wait_for_ready(self):

        print("Waiting for connection...")

        try:
            self.conn = self.listener.accept()
            print('Connection accepted from', self.listener.last_accepted)
        except OSError:
            if not self.isClosed:
                print("Exception while accepting new connection")
                self.listener.close()
            # else - that's fine, the transfer was explicitly closed.

    def close(self):
        if not self.isClosed:
            self.isClosed = True
            self.listener.close()

    def send(self, message):
        if self.conn is None:
            raise RuntimeError("Connection was not established.")

        try:
            self.conn.send(message)
            return True
        except ConnectionError:
            print("Connection broken :(")
            self.conn = None
            return False

    def is_ready(self):
        return self.conn is not None
