import queue
import time
import csv
import sys
import numpy as np
import datetime
import logging



if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s- %(levelname)s [%(thread)s] %(message)s",
        handlers=[
            # logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.debug('This message is skipped as a level is set as INFO')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('Testing non-ASCII character, Ø and ö')

