import re
import jsonlines
import json
from copy import deepcopy
from collections import defaultdict
import tqdm
import logging

logger = logging.getLogger(__name__)

def init_logging(debug=False):
    LEVEL = logging.DEBUG if debug else logging.INFO
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(format=format_str, level=LEVEL)

delete_list = ["&gt;", "&gt", "¡ª", "-- '''"]
punctuations = [r" ?", r" !", r" .", r" ,"]


def recover_lower_case(text):
    # capitalize the first character
    text = text[0].upper() + text[1:]
    # capitalize ?!.
    text = re.sub(r"(?<=[\.?!]\s+)\w", lambda pat: pat.group(0).upper(), text)
    # capitalize I (match ', end, space)
    text = re.sub(r"(?<=\s+)i(?=('|$|\s))", lambda pat: pat.group(0).upper(), text)

    return text


def one_dialogue_delete_empty_sentence(dialogue):
    flag = True
    while (flag):
        flag = False
        for idx in range(len(dialogue)):
            if str(dialogue[idx][1]) == "nan" or str(dialogue[idx][1]).strip() == "" or dialogue[idx][1] == None or \
                    dialogue[idx][1] == "[removed]":
                del dialogue[idx]
                flag = True
                break

    return dialogue


def abandon_dialogue_containinig_empty_sentence(dialogue):
    flag = True

    for idx in range(len(dialogue)):
        # reminder: do not use str(dialogue[idx][1])==None
        if str(dialogue[idx][1]) == "nan" or str(dialogue[idx][1]).strip() == "" or dialogue[idx][1] == None or \
                dialogue[idx][1] == "[removed]" or dialogue[idx][1] == "[deleted]":
            flag = False
            break

    return flag


def delete_empty_sentence(all_dialogue):
    # all_dialogue = [one_dialogue_delete_empty_sentence(one) for one in all_dialogue]
    all_dialogue = [one for one in all_dialogue if abandon_dialogue_containinig_empty_sentence(one)]
    return all_dialogue


# may not be useful
def one_dialogue_merge_same_person(dialogue):
    flag = True
    while (flag):
        flag = False
        for idx in range(len(dialogue) - 1):
            if dialogue[idx][0] == dialogue[idx + 1][0]:
                dialogue[idx][1] = dialogue[idx][1].strip() + " " + dialogue[idx + 1][1].strip()
                del dialogue[idx + 1]
                flag = True
                break
    return dialogue


def merge_same_person(all_dialogue):
    all_dialogue = [one_dialogue_merge_same_person(one) for one in all_dialogue]
    return all_dialogue


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


def delete_one_sentence_dialogue(all_dialogue):
    all_dialogue = [one for one in all_dialogue if len(one) > 1]
    return all_dialogue


def capitalize_i(sentence):
    for idx in range(1, len(sentence) - 1):
        if sentence[idx - 1:idx + 2] == " i ":
            sentence = sentence[:idx] + "I" + sentence[idx + 1:]
    return sentence


def add_persons(all_dialogue):
    for idx in range(len(all_dialogue)):
        for jdx in range(len(all_dialogue[idx])):
            if jdx % 2 == 0:
                all_dialogue[idx][jdx] = ["A", all_dialogue[idx][jdx]]
            if jdx % 2 == 1:
                all_dialogue[idx][jdx] = ["B", all_dialogue[idx][jdx]]
    return all_dialogue


def delete(delete_list, text):
    for one in delete_list:
        text.replace(one, "")
    return text


def process_single_text(text):
    text = text.strip()

    # weird unicode bug
    text = re.sub(u"(\u2018|\u2019)", "'", text)
    # replace to EN dash
    text = re.sub(u"\u2014", "-", text)
    text = re.sub(u"\u2013", "-", text)
    # pound money symbol and en money symbol
    text = re.sub(u"(\u00a3|\u20ac)", "$", text)
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

    text = delete(delete_list, text)

    # delete extra blankspack
    text = re.sub(' +', ' ', text)

    # concatenate 's
    text = re.sub(" +'s +", "\'s ", text)

    # process punct
    text = text.replace("a . m .", "a.m."). \
        replace("p . m .", "p.m.").replace(" .", ".") \
        .replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
    text = re.sub(r"\?+", "?", text)
    text = re.sub(r"\!+", "!", text)

    # process multiple "\n"
    text = re.sub(r"\s*\n+", " ", text)

    # upper first letter

    if text[0].islower():
        text = text[0].upper() + text[1:]

    # upper first char of other sentences
    text = re.sub(r"(?<=[\.?!]\s)\w", lambda pat: pat.group(0).upper(), text)
    # capitalize "i"
    text = re.sub(r"(?<=\s)i(?=('|$|\s))", lambda pat: pat.group(0).upper(), text)

    # other
    text = re.sub('( -)$', '', text)
    text = re.sub('( --)$', '', text)
    text = text.strip()
    text = re.sub('(?<=\w)(—)$', '', text)

    # text = capitalize_i(text)

    if False:
        for kdx in range(len(text) - 2):
            if text[kdx] in "?!,." and text[kdx + 1] == " ":
                if text[kdx + 2].islower():
                    if kdx > 3 and text[kdx - 3:kdx + 1] not in ["a.m.", "p.m."]:
                        text = all_dialogue[idx][jdx][1][:kdx + 2] + \
                               text[kdx + 2].upper() + \
                               text[kdx + 3:]

    return text


def process_unusual_unicode(text):

    # weird unicode bug
    text = re.sub(u"(\u2018|\u2019)", "'", text)
    # replace to EN dash
    text = re.sub(u"\u2014", "-", text)
    text = re.sub(u"\u2013", "-", text)
    # pound money symbol and en money symbol
    text = re.sub(u"(\u00a3|\u20ac)", "$", text)
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


def process_all_dialogue_text(all_dialogue):
    flag = True
    for idx in range(len(all_dialogue)):
        for jdx in range(len(all_dialogue[idx])):
            try:
                all_dialogue[idx][jdx][1] = process_single_text(all_dialogue[idx][jdx][1])
            except:
                print(idx, jdx)
                print(all_dialogue[idx][jdx])

    return all_dialogue


def process_dialogue(all_dialogue):
    all_dialogue = delete_one_sentence_dialogue(all_dialogue)
    all_dialogue = delete_empty_sentence(all_dialogue)
    all_dialogue = process_all_dialogue_text(all_dialogue)

    # all_dialogue = merge_same_person(all_dialogue)

    return all_dialogue


def del_multiple(l, index):
    for one in reversed(index):
        del l[one]

    return l


def split_by_index(all_dialogue, index):
    new_dialogue = []
    for idx in range(len(index) - 1):
        start = index[idx]
        end = index[idx + 1]
        new_dialogue.append(all_dialogue[start:end])
    return new_dialogue


def replace_http(text):
    pattern = re.compile(r"https?://[\S]{4}[\S]*")
    text = re.sub(pattern, "URL", text)
    return text


def get_dialogue_from_text_and_user(all_dialogue):
    print("this function is only for convkit dataset, which has keys \"text\" and \"user\"")
    new_dialogue = []
    for one in all_dialogue:
        one_dialogue = []
        for sent in one:
            one_dialogue.append([sent["user"], sent["text"]])
        new_dialogue.append(one_dialogue)

    return new_dialogue


def convokit_extract_user_and_text(all_dialogue):
    new_all_dialogue = []
    for one_dialogue in all_dialogue:
        new_one_dialogue = [[one["user"], one["text"]] for one in one_dialogue]
        new_all_dialogue.append(new_one_dialogue)
    return new_all_dialogue


def add_dialogue_index(prefix, all_dialogue):
    return {prefix + "_" + str(idx): all_dialogue[idx] for idx in range(len(all_dialogue))}


def convokit_split_dialogue_by_root(all_dialogue):
    logger.info("spliting dialogue .....")
    root_dict = defaultdict(list)
    for one_dialogue in all_dialogue:
        root_ = one_dialogue["root"]
        root_dict[root_].append(one_dialogue)

    logger.info("done split dialogue")
    return [value for key, value in root_dict.items()]


def convokit_extract_user_and_text_not_used_right_now(all_dialogue):
    # this is used with convokit_find_longest_two_person_sequence

    logger.info("extracting user and text....")

    print("this is used with convokit_find_longest_two_person_sequence")

    new_all_dialogue = []
    for one_dialogue in all_dialogue:

        new_one_dialogue = convokit_find_longest_two_person_sequence(one_dialogue)
        if new_one_dialogue != 0:
            new_one_dialogue = [[one["user"], one["text"]] for one in new_one_dialogue]
            new_all_dialogue.append(new_one_dialogue)

    logger.info("done extract user and text....")
    return new_all_dialogue


def convokit_find_longest_two_person_sequence(one_dialogue):
    # one_dialogue = all_dialogue[2]

    # this is used to extraced two-persons conversations from multi-person dialogue

    id_to_utterance_dict = {one["id"]: one for one in one_dialogue}

    id_whole_set = set()
    for one in one_dialogue:
        id_whole_set.add(one['id'])

    id_leaf_set = deepcopy(id_whole_set)

    for one in one_dialogue:
        id_leaf_set.discard(one["reply-to"])

    # find trace for each leaf id
    id_trace = defaultdict(list)
    id_trace_name = defaultdict(list)
    for one_id in id_leaf_set:
        present = one_id
        while (present in id_whole_set):
            id_trace[one_id].append(present)

            name_ = id_to_utterance_dict[present]["user"]
            id_trace_name[one_id].append(name_)

            present = id_to_utterance_dict[present]["reply-to"]

    del_keys = []
    for key, value in id_trace_name.items():
        if len(set(value)) != 2:
            del_keys.append(key)

    for key in del_keys:
        del id_trace[key]

    if len(id_trace) != 0:
        final_trace = max([value for key, value in id_trace.items()], key=len)
        final_trace.reverse()
        return [id_to_utterance_dict[one_id] for one_id in final_trace]
    else:
        return 0


def convert_all_dialogue_from_dict_to_list(all_dialogue):
    return [value for key, value in all_dialogue.items()]


def read_jsonline(file):
    with jsonlines.open(file) as reader:
        objs = []
        i = 0
        for obj in reader:
            i = i + 1
            objs.append(obj)

    return objs


def read_json(file):
    with open(file, "r") as fp:
        return json.load(fp)


def delete_words(delete_list, text):
    for item in delete_list:
        text = text.replace(item, "")
    return text


def safe_clean_text(text):
    """ This is a safe text cleaning procedure for all datasets
    """
    # weird words
    text = delete_words(delete_list, text)

    # handle \\\'t \\\'ve
    text = text.replace(r"\\", "")

    # http
    text = replace_http(text)
    text = process_unusual_unicode(text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # fix puncutations
    for p in punctuations:
        text = text.replace(p, p[1:])
    text = re.sub(" (\u2018|\u2019|') ", r"\1", text)

    # replace to EN dash
    text = re.sub(u"\u2014", "-", text)
    text = re.sub(u"\u2013", "-", text)

    return text


def safe_clean_all_dialogue(all_dialogue):

    use_tqdm = False

    if use_tqdm:
        for idx in tqdm.tqdm(range(len(all_dialogue))):
            for jdx in range(len(all_dialogue[idx])):
                try:
                    all_dialogue[idx][jdx][1] = safe_clean_text(all_dialogue[idx][jdx][1])
                    #print(all_dialogue[idx][jdx][1])
                except:
                    print(idx, jdx)
                    print(all_dialogue[idx][jdx])
    else:
        for idx in range(len(all_dialogue)):
            for jdx in range(len(all_dialogue[idx])):
                try:
                    all_dialogue[idx][jdx][1] = safe_clean_text(all_dialogue[idx][jdx][1])
                    #print(all_dialogue[idx][jdx][1])
                except:
                    print(idx, jdx)
                    print(all_dialogue[idx][jdx])

    return all_dialogue


def save_json(data, file):
    with open(file, "w") as fp:
        json.dump(data, fp, indent=4)

# for different dataset, it could use different function as parameter
def process_all_dialogue_with_certain_text_process_function(function, all_dialogue):

    use_tqdm = False
    if use_tqdm:
        for idx in tqdm.tqdm(range(len(all_dialogue))):
            for jdx in range(len(all_dialogue[idx])):
                try:
                    all_dialogue[idx][jdx][1] = function(all_dialogue[idx][jdx][1])
                    #print(all_dialogue[idx][jdx][1])
                except:
                    print(idx, jdx)
                    print(all_dialogue[idx][jdx])
    else:
        for idx in range(len(all_dialogue)):
            for jdx in range(len(all_dialogue[idx])):
                try:
                    all_dialogue[idx][jdx][1] = function(all_dialogue[idx][jdx][1])
                    #print(all_dialogue[idx][jdx][1])
                except:
                    print(idx, jdx)
                    print(all_dialogue[idx][jdx])


    return all_dialogue


def delete_double_dash_all_dialogue(all_dialogue):
    for idx in range(len(all_dialogue)):
        for jdx in range(len(all_dialogue[idx])):
            try:

                text = all_dialogue[idx][jdx][1]
                text = text.strip()
                text = re.sub('(--)$', '', text)
                text = re.sub('(-)$', '', text)
                # text = text.replace("--", ",")
                # text = text.replace("-", ",")
                text = text.strip()
                all_dialogue[idx][jdx][1] = text
            except:
                print(idx, jdx)
                print(all_dialogue[idx][jdx])
    # print("done")
    return all_dialogue

# this is only for wiki-corpus dataset
def wiki_corpus_extra_text_process(all_dialogue):

    def text_process(text):
        pattern_wikicorpus = re.compile("-*''+<(.)+>")
        text = re.sub(pattern_wikicorpus, " ", text)

        pattern_wikicorpus_2 = re.compile("--+'*<(.)+>")
        text = re.sub(pattern_wikicorpus_2, " ", text)

        pattern_wikicorpus_3 = re.compile("(-+ *'+)$")
        text = re.sub(pattern_wikicorpus_3, " ", text)

        pattern_wikicorpus_4 = re.compile("'''[[][[](.)+(<sub>)$")
        text = re.sub(pattern_wikicorpus_4, " ", text)

        pattern_wikicorpus_5 = re.compile(r"([[]http[^\s]+) +((.)+)\]$")
        text = re.sub(pattern_wikicorpus_5, lambda pat: pat.group(2), text)

        pattern_wikicorpus_6 = re.compile(r"([[]http[^\s]+) +((.)+?)\]")
        text = re.sub(pattern_wikicorpus_6, lambda pat: pat.group(2), text)

        pattern_wikicorpus_5 = re.compile(r"([[]http[^\s]+)\]")
        text = re.sub(pattern_wikicorpus_5, "", text)

        pattern_wikicorpus_6 = re.compile(r"([[(]https?:\\[^\s]+)")
        text = re.sub(pattern_wikicorpus_6, "", text)

        pattern_wikicorpus_6 = re.compile(r"(https?:\\[^\s]+)")
        text = re.sub(pattern_wikicorpus_6, "URL", text)

        pattern_wikicorpus_6 = re.compile(r"<small(.)$")
        text = re.sub(pattern_wikicorpus_6, "", text)

        pattern_wikicorpus_6 = re.compile(r"<span(.)$")
        text = re.sub(pattern_wikicorpus_6, "", text)



        text = text.replace("\\\"", "\"")
        text = text.replace("\"\\", "\"")
        return text

    return process_all_dialogue_with_certain_text_process_function(text_process, all_dialogue)