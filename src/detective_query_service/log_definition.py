# import standard modules
import logging

# Set logging source
logging.basicConfig()
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

# file handler is commented out, since at the moment the logs need to appear in stream
# file_handler = logging.FileHandler('testfile.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
