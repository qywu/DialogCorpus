import json
import os, sys
import tqdm
import logging

logger = logging.getLogger(__name__)

# go to parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils import *

if __name__ == "__main__":
    init_logging()

    with open("daily_dialog/data/dialogues_text.txt") as fp:
        all_dialogue = fp.readlines()

    all_dialogue = [one.strip().split("__eou__") for one in all_dialogue]
    all_dialogue = [one[:-1] if one[-1] == "" else one for one in all_dialogue]

    new_all_dialog = []

    logger.info("Processing Daily Dialog Dataset")
    
    for dialog in tqdm.tqdm(all_dialogue):
        new_dialog = []
        for turn in dialog:
            turn = safe_clean_text(turn)
            new_dialog.append(turn)

        new_all_dialog.append(new_dialog)

    new_all_dialog = add_persons(new_all_dialog)
    new_all_dialog = add_dialogue_index("daily_dialogue", new_all_dialog)


    
    file_path = os.path.join(current_dir, "data/daily_dialog.json")
    logger.info(f"Saving Daily Dialog data to {file_path}")
    # save the data
    save_as_json(new_all_dialog, file_path)