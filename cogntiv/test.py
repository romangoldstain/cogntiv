import queue
import time

if __name__ == '__main__':
    start = time.perf_counter()
    i = 0
    while time.perf_counter() - start < 0.001:
        i += 1

    before = time.perf_counter()
    for j in range(9000):
        time.perf_counter()
    after = time.perf_counter()

    print(f'i={i}')
    print(f'i={after - before}')



"""
https://www.webucator.com/article/python-clocks-explained/
"""