import os, sys
# go to parent directory
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import json
import pandas as pd
import jsonlines
from util_jing import*
# from utils import*
from copy import deepcopy
from collections import defaultdict
import tqdm
import logging

init_logging()
logger = logging.getLogger(__name__)

dataset_name = "conversations-gone-awry-corpus"

def delete_double_equation_sign_sentence(text):
    if text.strip().startswith("==") and text.strip().endswith("=="):
        text = ""
    return text

raw_data = read_jsonline("full/conversations-gone-awry-corpus/utterances.jsonl")

all_dialogue = convokit_split_dialogue_by_root(raw_data)
all_dialogue = convokit_extract_user_and_text(all_dialogue)
all_dialogue = delete_more_persons_dialogue(all_dialogue)

# only for this dataset
all_dialogue = process_all_dialogue_with_certain_text_process_function(delete_double_equation_sign_sentence, all_dialogue)

all_dialogue = delete_one_sentence_dialogue(all_dialogue)
all_dialogue = delete_empty_sentence(all_dialogue)
all_dialogue = delete_one_turn_dialogue(all_dialogue)
all_dialogue = safe_clean_all_dialogue(all_dialogue)



logger.info("Processing " + dataset_name)
all_dialogue = add_dialogue_index(dataset_name, all_dialogue)

save_path = current_dir + "/data/" + dataset_name + ".json"
logger.info(f"Saving dataset to {save_path}")
save_json(all_dialogue, save_path)
