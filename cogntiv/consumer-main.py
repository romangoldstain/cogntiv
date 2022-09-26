import queue
from common.socket_transfer import SocketTransferClient
from consumer.matrix_worker import MatrixWorker
from consumer.receiver import Receiver
from consumer.matrix_analyzer import MatrixAnalyzer
from consumer.csv_writer import CSVWriter

if __name__ == '__main__':

    bus = queue.Queue(100)

    analyzer = MatrixAnalyzer()
    consumer = CSVWriter()
    Receiver(SocketTransferClient('localhost', 6000), bus).start()
    MatrixWorker(bus, 100, analyzer, consumer).start().join()


"""
Back-pressure path
1. Consumer - file write won't keep up.
2. Consumer - messages bus fills up.
3. Consumer - recv. buffer socket fill up.
4. Producer - send buffer socket fills up.
5. Producer - dispatcher blocks.
6. Producer - bus fills up; No new vectors created. 
"""