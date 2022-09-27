import sys
import logging
from multiprocessing import Process
import consumer_main
import producer_main
import common.socket_transfer as socket_transfer
from common.packet_loss import LossPolicy


def pick_loss_policy():
    if len(sys.argv) >= 2 and sys.argv[1] == '--noisy':
        logging.info('Noisy mode ON')
        return LossPolicy.within_interval(2, 3)

    return LossPolicy.never()


TCP_PORT = 6000

if __name__ == '__main__':
    """
    Spawn consumer and producer processes.
    """

    trans_server = socket_transfer.ServerSocketTransfer('localhost', TCP_PORT, pick_loss_policy())
    trans_client = socket_transfer.SocketTransferClient('localhost', TCP_PORT)

    producer = Process(target=producer_main.start_producer, args=(trans_server,))
    producer.start()

    producer = Process(target=consumer_main.start_consumer, args=(trans_client,))
    producer.start()

    producer.join()


"""
Back-pressure path
1. Consumer - file write won't keep up.
2. Consumer - messages bus fills up.
3. Consumer - recv. buffer socket fill up.
4. Producer - send buffer socket fills up.
5. Producer - dispatcher blocks.
6. Producer - bus fills up; No new vectors created. 
"""
