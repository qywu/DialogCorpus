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

_punctuations = [r"?", r"!", r".", r","]


def add_ending_punc(text):
    text = text.strip()
    if text[-1] not in _punctuations:
        text = text + "."
    return text


def merge_messages(message):
    texts = [item['text'] for item in message]
    texts = [add_ending_punc(item) for item in texts if len(item) > 0]
    senders = [item['sender'] for item in message]

    assert len(set(senders)) == 1

    return " ".join(texts)


if __name__ == "__main__":

    with open("CCC/data/dataset.json", "r") as f:
        raw_dialogs = json.load(f)

    logger.info("Processing CCC Dataset!")

    all_dialogs = []
    flag = True

    for dialog in tqdm.tqdm(raw_dialogs.values()):
        one_dialog = []
        for turn in dialog['messages']:
            text = merge_messages(turn)
            if len(text.split()) > 256:
                flag = False
                break
            one_dialog.append(safe_clean_text(text))

        if flag:
            if len(one_dialog) > 2:
                all_dialogs.append(one_dialog)
        else:
            flag = True

    all_dialogs = add_persons(all_dialogs)
    all_dialogs = add_dialogue_index("ccc", all_dialogs)

    # save the data
    file_path = os.path.join("CCC/data/CCC.json")
    logger.info("Saving CCC Dataset")
    save_as_json(all_dialogs, file_path)