import numpy as np
import time
from datetime import datetime
import queue
from multiprocessing.connection import Listener

from common.socket_transfer import SocketTransfer
from producer.vectory_factory import VectorFactory
from producer.vector_faucet import VectorFaucet
from producer.dispatcher import Dispatcher

next_drop = -1


def maybe_drop(elapsed):
    global next_drop
    if next_drop == -1:
        next_drop = elapsed + np.random.uniform(2, 3, 1)[0]

    if elapsed >= next_drop:
        next_drop = elapsed + np.random.uniform(2, 3, 1)[0]
        return True

    return False


def main(q):
    started_at = datetime.now()

    while True:

        arr = VectorFactory().create()
        elapsed = (datetime.now() - started_at).seconds
        if maybe_drop(elapsed):
            arr = []

        # print('%s %s' % (elapsed, arr))
        q.put(arr)

        time.sleep(1)


def listen(q):
    address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
    listener = Listener(address)
    conn = listener.accept()
    print('connection accepted from', listener.last_accepted)
    while True:
        item = q.get()
        conn.send(item);
        print(f'SENT {item}')
        q.task_done()
    # while True:
    #     msg = conn.recv()
    #     # do something with msg
    #     if msg == 'close':
    #         conn.close()
    #         break
    # listener.close()
    # pass


if __name__ == '__main__':
    bus = queue.Queue(100)

    faucet = VectorFaucet(VectorFactory(), bus)
    transfer = SocketTransfer('localhost', 6000)
    dispatcher = Dispatcher(transfer, bus)

    dispatcher.start()
    faucet.start().join()

    # create vectory factory
    # create faucet (factory, vector bus)
    #
    # create dropper
    # create transfer (common)
    # create dispatcher(dropper, transfer, bus)
