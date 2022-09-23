import queue
from common.socket_transfer import SocketTransfer
from common.rate_monitor import RateMonitor
from producer.vectory_factory import VectorFactory
from producer.vector_faucet import VectorFaucet
from producer.dispatcher import Dispatcher


if __name__ == '__main__':
    bus = queue.Queue(100)

    faucet = VectorFaucet(VectorFactory(), bus)
    dispatcher = Dispatcher(SocketTransfer('localhost', 6000), RateMonitor(), bus)

    dispatcher.start()

    print(f'Vector faucet is running...')
    faucet.start().join()
