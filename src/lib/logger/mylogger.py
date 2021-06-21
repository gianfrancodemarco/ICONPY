import logging
import os

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.addHandler(ch)

# file handler
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../debug.log')
fh = logging.FileHandler(filename)

#logger.addHandler(fh)
