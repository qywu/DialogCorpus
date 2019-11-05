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

    with open("frames/data/frames_data.json", "r") as f:
        raw_dialogs = json.load(f)

    logger.info("Processing Frames Dataset")

    all_dialogs = []

    for dialog in tqdm.tqdm(raw_dialogs):
        one_dialog = []
        rating = dialog['labels']['userSurveyRating']

        for turn in dialog['turns']:
            one_dialog.append([turn['author'], safe_clean_text(turn['text'])])

        all_dialogs.append(one_dialog)

    all_dialogs = add_dialogue_index("frames", all_dialogs)

        # save the data
    file_path = os.path.join("frames/data/frames.json")
    logger.info("Saving Frames Dataset")
    save_as_json(all_dialogs, file_path)