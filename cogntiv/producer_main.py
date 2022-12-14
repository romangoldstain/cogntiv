import queue
import logging
from common.socket_transfer import ServerSocketTransfer
from common.rate_monitor import RateMonitor
from common.packet_loss import LossPolicy
from producer.vectory_factory import VectorFactory
from producer.vector_faucet import VectorFaucet
from producer.dispatcher import Dispatcher
from common.conf_logger import apply_log_conf


def start_producer(transfer):
    apply_log_conf()

    bus = queue.Queue(100)
    faucet = VectorFaucet(VectorFactory(), bus)
    dispatcher = Dispatcher(transfer, RateMonitor(), bus)

    faucet.start()
    logging.info('Vector faucet is running. Starting dispatcher and waiting for clients...')

    dispatcher.start().join()


if __name__ == '__main__':

    start_producer(ServerSocketTransfer('localhost', 6000, LossPolicy.never()))
