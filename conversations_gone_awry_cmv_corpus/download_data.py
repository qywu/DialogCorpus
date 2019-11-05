import json
import os, sys
import tqdm
import logging
from zipfile import ZipFile

# go to parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils import *

url = "https://zissou.infosci.cornell.edu/convokit/datasets/conversations-gone-awry-cmv-corpus/full.corpus"
file_dir = "conversations_gone_awry_cmv_corpus/data"

init_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, "full.corpus")
    logger.info("Downloading Conversations-gone-awry-cmv file!")
    http_get_file(url, file_path)

    with ZipFile(file_path, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(file_dir)