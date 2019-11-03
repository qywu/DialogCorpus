import json
import os, sys
import tqdm
import logging

# go to parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils import *

url = "https://s3.amazonaws.com/datasets.huggingface.co/personachat/personachat_self_original.json"
file_dir = "persona_chat/data"

init_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, "personachat_self_original.json")
    logger.info("Downloading Persona-Chat file!")
    http_get_file(url, file_path)
