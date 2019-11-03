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

    data_dir = "schema_dialog/data/dstc8-schema-guided-dialogue/train"

    all_dialogs = []

    for file_name in tqdm.tqdm(os.listdir(data_dir)):
        
        if 'schema.json' in file_name:
            continue

        file_path = os.path.join(data_dir, file_name)
        
        with open(file_path, "r") as f:
            data = json.load(f)
            
        part_dialogs = []
        
        for dialog in data:
            one_dialog = [[item['speaker'].capitalize(), item['utterance']]  for item in dialog['turns']]
            part_dialogs.append(one_dialog)
        
        all_dialogs.extend(part_dialogs)


    all_dialogs = add_dialogue_index("schema_dialog", all_dialogs)
    
    # save the data
    file_path = os.path.join(current_dir, "data/schema_dialog.json")
    logger.info(f"Saving Schema Dialog data to {file_path}")
    save_as_json(all_dialogs, file_path)