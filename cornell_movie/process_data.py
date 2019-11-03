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

    # get all dialog mapping
    with open("cornell_movie/data/movie_conversations.txt", "r") as f:
        dialog_mapping = f.readlines()

    dialog_mapping = [eval(item.split("+++$+++")[3]) for item in dialog_mapping]

    # get raw dialog lines
    with open(
        "cornell_movie/data/movie_lines.txt",
        "r",
        encoding='utf-8',
        errors='ignore'
    ) as f:
        raw_dialog_lines = f.readlines()

    logger.info("Processing Cornell Movie Dataset")
    raw_dialog_dict = {}

    for line in tqdm.tqdm(raw_dialog_lines):
        items = line.split("+++$+++")
        raw_dialog_dict[items[0].strip()] = [
            items[3].strip().capitalize(),
            safe_clean_text(items[4])
        ]

    all_dialog = []

    for i in range(len(dialog_mapping)):
        one_dialog = []
        for key in dialog_mapping[i]:
            one_dialog.append(raw_dialog_dict[key])
        all_dialog.append(one_dialog)

    all_dialog = add_dialogue_index("cornell_movie", all_dialog)

    # save the data
    file_path = os.path.join("cornell_movie/data/cornell_movie.json")
    logger.info("Saving Cornell Movie Dataset")
    save_as_json(all_dialog, file_path)