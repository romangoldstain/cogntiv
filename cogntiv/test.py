import queue
import time
import csv
import numpy as np
import datetime

if __name__ == '__main__':

    x = np.matrix(np.arange(12).reshape((3, 4)))
    ll = x.std(0)[0].tolist()

    m = {'key1': 'value1', 'key2': 'value2'}
    print(f'out={m.values()}')

    arr = [1, 2, 3]
    arr.extend(ll)
    print(f'out={arr}')

    print(datetime.datetime.now().strftime("%Y%m%d_%H%M_%S_results"))


