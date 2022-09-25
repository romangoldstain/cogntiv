import sys
import queue
from common.socket_transfer import SocketTransfer
from common.rate_monitor import RateMonitor
from common.packet_loss import LossPolicy
from producer.vectory_factory import VectorFactory
from producer.vector_faucet import VectorFaucet
from producer.dispatcher import Dispatcher


if __name__ == '__main__':

    if len(sys.argv) >= 2 and sys.argv[1] == '--noisy':
        print(f'Noisy mode ON')
        loss_policy = LossPolicy.within_interval(2, 3)
    else:
        loss_policy = LossPolicy.never()

    bus = queue.Queue(100)
    faucet = VectorFaucet(VectorFactory(), bus)
    dispatcher = Dispatcher(SocketTransfer('localhost', 6000, loss_policy), RateMonitor(), bus)

    dispatcher.start()

    print(f'Vector faucet is running...')
    faucet.start().join()
