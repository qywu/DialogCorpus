import json
import os, sys
import tqdm
import logging

# go to parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils import *

url = "https://raw.githubusercontent.com/BYU-PCCL/chitchat-dataset/master/dataset.json"
file_dir = "CCC/data"

init_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, "dataset.json")
    logger.info("Downloading Chit-Chat Challenge file!")
    http_get_file(url, file_path)
