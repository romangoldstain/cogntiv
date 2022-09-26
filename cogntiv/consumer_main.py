import queue
from common.socket_transfer import SocketTransferClient
from consumer.matrix_worker import MatrixWorker
from consumer.receiver import Receiver
from consumer.matrix_analyzer import MatrixAnalyzer
from consumer.csv_writer import CSVWriter


def start_consumer():
    bus = queue.Queue(100)

    analyzer = MatrixAnalyzer()
    consumer = CSVWriter()
    Receiver(SocketTransferClient('localhost', 6000), bus).start()
    MatrixWorker(bus, 100, analyzer, consumer).start().join()


if __name__ == '__main__':
    start_consumer()