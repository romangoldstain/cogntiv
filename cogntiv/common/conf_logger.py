import logging
import sys


def apply_log_conf():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s [%(thread)s] %(message)s",
        handlers=[
            # logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
