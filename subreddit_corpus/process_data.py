import json
import os, sys
from collections import defaultdict
import tqdm
import logging

# go to parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils import *


def check_two_persons(one_dialogue):
    name = set([one[0] for one in one_dialogue])
    if len(set(name)) != 2:
        return False
    else:
        return True


def delete_more_persons_dialogue(all_dialogue):
    flag = True
    while flag:
        flag = False
        for idx in range(len(all_dialogue)):
            if not check_two_persons(all_dialogue[idx]):
                del all_dialogue[idx]
                flag = True
                break
    return all_dialogue


def delete_one_turn_dialogue(all_dialogue):
    all_dialogue = [one for one in all_dialogue if len(one) > 2]
    return all_dialogue


def abandon_dialogue_containinig_empty_sentence(dialogue):

    for idx in range(len(dialogue)):
        # reminder: do not use str(dialogue[idx][1])==None
        if str(dialogue[idx][1]) == "nan" or str(dialogue[idx][1]).strip() == "" or dialogue[idx][1] == None or \
                "[removed]" in dialogue[idx][1] or "[deleted]" in dialogue[idx][1]:
            return False

        if "[(G)](URL)" in dialogue[idx][1]:
            return False

    return True


def delete_empty_sentence(all_dialogue):
    # all_dialogue = [one_dialogue_delete_empty_sentence(one) for one in all_dialogue]
    all_dialogue = [
        one for one in all_dialogue
        if abandon_dialogue_containinig_empty_sentence(one)
    ]
    return all_dialogue


def convokit_split_dialogue_by_root(all_dialogue):
    logger.info("spliting dialogue .....")
    root_dict = defaultdict(list)
    for one_dialogue in all_dialogue:
        root_ = one_dialogue["root"]
        root_dict[root_].append(one_dialogue)

    logger.info("done split dialogue")
    return [value for key, value in root_dict.items()]


def convokit_extract_user_and_text(all_dialogue):
    new_all_dialogue = []
    for one_dialogue in tqdm.tqdm(all_dialogue):
        # clean the text here
        new_one_dialogue = [clean_text(one["text"]) for one in one_dialogue]
        new_all_dialogue.append(new_one_dialogue)
    return new_all_dialogue


def process_unusual_unicode(text):
    text = text.replace("\u2022", "")
    # weird unicode bug
    text = re.sub(u"(\u2018|\u2019)", "'", text)
    # replace to EN dash
    text = re.sub(u"\u2014", "-", text)
    text = re.sub(u"\u2013", "-", text)
    # "“" and "”"
    text = re.sub(u"(\u201c|\u201d)", "\"", text)
    # middle point
    text = re.sub(u"\u00b7", ".", text)
    # three middle point
    text = re.sub(u"\u2026", " ", text)
    # Vulgar Fraction One Half
    text = re.sub(u"\u00bd", ".5 ", text)
    # Vulgar Fraction three quarters
    text = re.sub(u"\u00be", ".75 ", text)
    # Latin Small Letter E with Acute
    text = re.sub(u"(\u00e9|\u00e8|\u00ea)", "e", text)
    # ä
    text = re.sub(u"(\u00e4|\u00e0)", "a", text)
    # latin i
    text = re.sub(u"\u00ef|\u00ee", "i", text)
    # ä
    text = re.sub(u"(\u00f4|\u00f6|\u00d6|\u00d4)", "o", text)
    # tempture and other
    text = re.sub(u"(\u00b0|\u00ba)", "", text)
    # 1/4
    text = re.sub(u"\u00bc", "", text)
    # another latin u. Making more sense when deleting it.
    text = re.sub(u"\0214", " ", text)
    text = re.sub(u"\00e7", ".75 ", text)
    text = re.sub(u"(\00c1|\u00e2)", "a", text)
    text = re.sub(u"\00ff", "y", text)
    text = re.sub(u"\u00df", "s", text)
    text = re.sub(u"\u017e", "z", text)
    text = re.sub(u"\0213", "r", text)
    text = re.sub(u"\00e7", "c", text)
    text = re.sub(u"\00f1", "n", text)
    text = re.sub(u"(\00fc|\u00f9)", "u", text)

    return text


def clean_text(text):
    text = replace_http(text)
    text = text.replace("\n", " ")
    text = process_unusual_unicode(text)
    text = text.replace("\\", "")
    text = text.replace("==", "")
    text = text.replace("''", "'")
    text = safe_clean_text(text)
    return text


init_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # from transformers import GPT2Tokenizer
    # tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    # text = "beyond with you instead \ud83d\ude0f"
    # breakpoint()

    with open("subreddit_corpus/data/reddit-corpus-small/utterances.json", encoding='utf-8') as f:
            all_turns = json.load(f)

    logger.info("Processing subreddit corpus Dataset")

    all_dialogs = []

    all_dialogs = convokit_split_dialogue_by_root(all_turns)
    all_dialogs = convokit_extract_user_and_text(all_dialogs)
    all_dialogs = add_persons(all_dialogs)
    all_dialogs = delete_more_persons_dialogue(all_dialogs)
    all_dialogs = delete_empty_sentence(all_dialogs)
    all_dialogs = delete_one_turn_dialogue(all_dialogs)

    all_dialogs = add_dialogue_index(
        "subreddit_corpus", all_dialogs
    )

    # save the data
    file_path = os.path.join(
        "subreddit_corpus/data/"
        "subreddit_corpus.json"
    )
    logger.info("Saving Subreddit Dataset")
    save_as_json(all_dialogs, file_path)

    # encode('utf-16', 'surrogatepass').decode('utf-16').encode('utf-8')