import logging
import logging.config
import json
from dotenv import load_dotenv
import os

load_dotenv()
logging.config.fileConfig(fname=os.getenv('CONFIG_PATH'))


# logging.basicConfig(
#      filename='logs/logs3.log',
#      level=logging.INFO, 
#      format="%(asctime)s %(levelname)s %(message)s",
#      datefmt='%H:%M:%S'
#  )

with open(os.getenv('ERROR_LIST', 'r')) as f:
        error_decoder = json.load(f)

logging.error(error_decoder['10'])