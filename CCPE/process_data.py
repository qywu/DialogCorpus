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

    with open("CCPE/data/CCPE-M-2019/data.json", "r") as f:
        raw_dialogs = json.load(f)

    all_dialogs = []

    logger.info("Processing CCPE Dataset")
    for dialog in raw_dialogs:
        one_dialog = []
        for turn in dialog['utterances']:
            one_dialog.append([turn['speaker'].capitalize(), turn['text']])
            
        all_dialogs.append(one_dialog)

    all_dialogs = add_dialogue_index("CCPE", all_dialogs)

    # save the data
    file_path = os.path.join("CCPE/data/CCPE.json")
    logger.info("Saving CCPE Dataset")
    save_as_json(all_dialogs, file_path)