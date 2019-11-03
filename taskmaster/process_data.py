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

    with open("taskmaster/data/TASKMASTER-1-2019/self-dialogs.json", "r") as f:
        self_dialogs = json.load(f)
        
    with open("taskmaster/data/TASKMASTER-1-2019/woz-dialogs.json", "r") as f:
        woz_dialogs = json.load(f)

    raw_dialogs = self_dialogs + woz_dialogs

    all_dialogs = []

    logger.info("Processing Task Master Dataset")
    for dialog in raw_dialogs:
        one_dialog = []
        for turn in dialog['utterances']:
            one_dialog.append([turn['speaker'].capitalize(), turn['text']])
            
        all_dialogs.append(one_dialog)

    all_dialogs = add_dialogue_index("taskmaster", all_dialogs)

    # save the data
    file_path = os.path.join("taskmaster/data/taskmaster.json")
    logger.info("Saving Task Master Dataset")
    save_as_json(all_dialogs, file_path)