import json
import os, sys
import tqdm
import logging

# go to parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils import *

init_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    data_dir = "self_dialog/data/self_dialogue_corpus/dialogues"

    all_dialogs = []

    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "r") as f:
            data = f.readlines()
        data = [item.strip() for item in data]
        # max_len = max([len(item.split()) for item in data])
        
        if len(data) < 4:
            continue
        
        all_dialogs.append(data)

    all_dialogs = add_persons(all_dialogs)
    all_dialogs = add_dialogue_index("self_dialog", all_dialogs)

    # save the data
    file_path = os.path.join(current_dir, "data/self_dialog.json")
    logger.info(f"Saving Self Dialog data to {file_path}")
    save_as_json(all_dialogs, file_path)