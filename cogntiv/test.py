import queue
import time

import numpy as np

if __name__ == '__main__':
    a1 = np.random.default_rng().random(2)
    a2 = np.random.default_rng().random(2)
    a3 = np.random.default_rng().random(2)

    cc = np.array(a1)


    m1 = np.matrix(cc)
    print(f'{m1}')
    print(f'{m1.std()} {m1.mean()}')