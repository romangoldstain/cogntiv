from multiprocessing.connection import Listener


class SocketTransfer:

    def __init__(self, address, port):
        self.address = (address, port)  # family is deduced to be 'AF_INET'
        self.conn = None
        self.listener = None
        self.isClosed = False

    def wait_for_ready(self):
        print("Waiting for connection...")
        self.listener = Listener(self.address)
        try:
            self.conn = self.listener.accept()
            print('Connection accepted from', self.listener.last_accepted)
        except OSError:
            if not self.isClosed:
                print("Exception while accepting new connection")
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
