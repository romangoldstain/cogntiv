import queue
import time

if __name__ == '__main__':
    bus = queue.Queue(100)
    bus.put('123')

    print(f'{bus.get()}')
    print(f'{bus.get()}')



"""
https://www.webucator.com/article/python-clocks-explained/
"""