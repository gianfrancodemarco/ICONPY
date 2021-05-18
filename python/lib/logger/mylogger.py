import logging
import os


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../../../Python Tesi/src/debug.log')

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(filename),
        logging.StreamHandler()
    ]
)