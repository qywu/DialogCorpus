import gdown
import os, sys
from zipfile import ZipFile
import logging

logger = logging.getLogger(__name__)

# go to parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils import *

git_url = "https://github.com/google-research-datasets/dstc8-schema-guided-dialogue.git"
file_dir = "schema_dialog/data"

if __name__ == "__main__":

    os.makedirs(file_dir, exist_ok=True)

    data_dir = os.path.join(parent_dir, file_dir)

    logger.info("Downloading Schema Dialog file!")

    os.chdir(data_dir)
    os.system(f"git clone {git_url}")


