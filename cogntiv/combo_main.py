import os
from multiprocessing import Pool
import consumer_main
import producer_main

def run_process(process):
    producer_main.start_producer()
    # os.system('python.exe {}'.format(process))


if __name__ == '__main__':
    processes = ('consumer_main.py', 'producer_main.py')

    pool = Pool(processes=2)
    pool.map(run_process, processes)


"""
Back-pressure path
1. Consumer - file write won't keep up.
2. Consumer - messages bus fills up.
3. Consumer - recv. buffer socket fill up.
4. Producer - send buffer socket fills up.
5. Producer - dispatcher blocks.
6. Producer - bus fills up; No new vectors created. 
"""
