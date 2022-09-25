import queue
from common.socket_transfer import SocketTransferClient
from consumer.matrix_worker import MatrixWorker
from consumer.receiver import Receiver
from consumer.matrix_analyzer import MatrixAnalyzer

if __name__ == '__main__':

    bus = queue.Queue(100)

    analyzer = MatrixAnalyzer()
    Receiver(SocketTransferClient('localhost', 6000), bus).start()
    MatrixWorker(bus, 100, analyzer).start().join()
