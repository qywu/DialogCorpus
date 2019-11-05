import os
import json
import regex as re
import requests
import tqdm
import logging

logger = logging.getLogger(__name__)

delete_list = ["&gt;", "&gt", "¡ª", "-- '''"]
punctuations = [r" ?", r" !", r" .", r" ,"]


def init_logging(debug=False):
    LEVEL = logging.DEBUG if debug else logging.INFO
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(format=format_str, level=LEVEL)


def delete_words(delete_list, text):
    for item in delete_list:
        text = text.replace(item, "")
    return text


def add_persons(all_dialogue):
    """
    Add role identification to the dialog
    """
    for idx in range(len(all_dialogue)):
        for jdx in range(len(all_dialogue[idx])):
            if jdx % 2 == 0:
                all_dialogue[idx][jdx] = ["A", all_dialogue[idx][jdx]]
            if jdx % 2 == 1:
                all_dialogue[idx][jdx] = ["B", all_dialogue[idx][jdx]]
    return all_dialogue


def add_dialogue_index(prefix, all_dialogue):
    return {
        prefix + "_" + str(idx): all_dialogue[idx]
        for idx in range(len(all_dialogue))
    }


def save_as_json(data, file):
    with open(file, "w", encoding='utf-8') as fp:
        json.dump(data, fp, indent=4)


def safe_clean_text(text):
    """ This is a safe text cleaning procedure for all datasets
    """
    # strip
    text = text.strip()

    # weird words
    text = delete_words(delete_list, text)

    # handle \\\'t \\\'ve
    text = text.replace(r"\\", "")

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # fix puncutations
    for p in punctuations:
        text = text.replace(p, p[1:])
    text = re.sub(" (\u2018|\u2019|') ", r"\1", text)

    # replace to EN dash
    text = re.sub(u"\u2014", "-", text)
    text = re.sub(u"\u2013", "-", text)

    return text


def http_get_file(url, file_name, proxies=None):
    logger.info(f"saving to {file_name}")
    req = requests.get(url, stream=True, proxies=proxies)
    content_length = req.headers.get('Content-Length')
    total = int(content_length) if content_length is not None else None
    progress = tqdm.tqdm(unit="B", total=total)

    with open(file_name, "wb") as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                progress.update(len(chunk))
                f.write(chunk)
    progress.close()


def recover_lower_case(text):
    # capitalize the first character
    text = text[0].upper() + text[1:]
    # capitalize ?!.
    text = re.sub(r"(?<=[\.?!]\s+)\w", lambda pat: pat.group(0).upper(), text)
    # capitalize I (match ', end, space)
    text = re.sub(
        r"(?<=\s+)i(?=('|$|\s))", lambda pat: pat.group(0).upper(), text
    )

    return text


def replace_http(text):
    pattern = re.compile(r"https?[\S]+[^\)|.|\s]")
    text = re.sub(pattern, "URL", text)
    return text