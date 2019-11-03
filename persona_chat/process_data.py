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
    with open("persona_chat/data/personachat_self_original.json") as fp:
        raw_data = json.load(fp)

    raw_data = raw_data["train"] + raw_data["valid"]
    all_dialog = [item['utterances'][-1]['history'] for item in raw_data]

    logger.info("Processing Persona-Chat data")

    new_all_dialog = []
    for dialog in tqdm.tqdm(all_dialog):
        new_dialog = []
        for turn in dialog:
            turn = recover_lower_case(turn)
            turn = safe_clean_text(turn)
            new_dialog.append(turn)

        new_all_dialog.append(new_dialog)

    breakpoint()

    # save the data
    file_path = os.path.join(current_dir, "data/persona_chat.json")
    logger.info(f"Saving Persona-Chat data to {file_path}")
    save_as_json(None, file_path)