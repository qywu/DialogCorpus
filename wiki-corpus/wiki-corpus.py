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
import re

init_logging()
logger = logging.getLogger(__name__)

from multiprocessing import Pool
import multiprocessing
cores = multiprocessing.cpu_count() * 3 // 4
P = Pool(cores)

def multiple_thread_method(fun, all_dialogue):
    new_all_dialogue = []
    all_dialogue = [[one] for one in all_dialogue]
    for one_dialogue in P.map(fun, all_dialogue):
        if one_dialogue != []:
            new_all_dialogue.append(one_dialogue[0])

    return new_all_dialogue


dataset_name = "wiki-corpus"

raw_data = read_json("full/wiki-corpus/utterances.json")

all_dialogue = convokit_split_dialogue_by_root(raw_data)
all_dialogue = convokit_extract_user_and_text(all_dialogue)
all_dialogue = delete_more_persons_dialogue(all_dialogue)
all_dialogue = multiple_thread_method(delete_double_dash_all_dialogue, all_dialogue)
logger.info("deleting double dash.....")
# all_dialogue = process_all_dialogue_with_certain_text_process_function(delete_double_dash, all_dialogue)
#def wrap_method(all_dialogue):
#    return process_all_dialogue_with_certain_text_process_function(delete_double_dash, all_dialogue)
logger.info("deleting dialogue that contain one sentence.....")
all_dialogue = multiple_thread_method(delete_one_sentence_dialogue, all_dialogue)

logger.info("deleting dialogue that contain empty sentence.......")
all_dialogue = multiple_thread_method(delete_empty_sentence, all_dialogue)

logger.info("deleting dialogue that contains only one turn")
all_dialogue = multiple_thread_method(delete_one_turn_dialogue, all_dialogue)

logger.info("safe cleaning all dialogue......")
all_dialogue = multiple_thread_method(safe_clean_all_dialogue, all_dialogue)

logger.info("adding index for dialogue.......")
all_dialogue = add_dialogue_index(dataset_name, all_dialogue)


data_dir = current_dir + "/data"
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
save_path = current_dir + "/data/" + dataset_name + ".json"
logger.info(f"Saving dataset to {save_path}")
save_json(all_dialogue, save_path)
