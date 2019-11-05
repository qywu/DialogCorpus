import argparse
import os
import json
import subprocess
import tqdm
import logging
from torchfly.utils import init_logging

init_logging()
logger = logging.getLogger(__name__)

datasets = [
    "CCC", "CCPE", "conversations_gone_awry_cmv_corpus",
    "conversations_gone_awry_corpus", "cornell_movie", "daily_dialog", "frames",
    "friends_corpus", "persona_chat", "schema_dialog", "self_dialog",
    "subreddit_corpus", "taskmaster"
]


def delete_one_turn_dialogs(all_dialogs):
    all_dialogs = {k: v for k, v in all_dialogs.items() if len(v) > 2}
    return all_dialogs


def prepare_data_command(dataset):
    download_command = f"python {dataset}/download_data.py"
    process_command = f"python {dataset}/process_data.py"
    return download_command, process_command


def join_all_data(file_name):
    logger.info("Join all datasets!")
    all_dialogs = {}

    for dataset in tqdm.tqdm(datasets):
        with open(f"{dataset}/data/{dataset}.json", "r") as f:
            dialogs = json.load(f)
            dialogs = delete_one_turn_dialogs(dialogs)
            all_dialogs.update(dialogs)

    with open(file_name, "w") as f:
        json.dump(all_dialogs, f, indent=4)


if __name__ == "__main__":
    # add parsing
    parser = argparse.ArgumentParser(description="Prepare data")
    parser.add_argument(
        '--download', action='store_true', help='If download the data'
    )
    parser.add_argument(
        '--process', action='store_true', help='If process the downloaded data'
    )
    parser.add_argument(
        '--join', action='store_true', help='If join all the processed data'
    )
    parser.add_argument(
        '--clean', action='store_true', help='Clean the processed data'
    )
    parser.add_argument(
        '--output_file_name',
        type=str,
        default="all_dialogs.json",
        help='File name for the final output'
    )

    args = parser.parse_args()

    # copy the current environment variables
    my_env = os.environ.copy()

    for dataset in datasets:
        # build commands
        download_command, process_command = prepare_data_command(dataset)

        if args.download:
            subprocess.call(download_command, shell=True, env=my_env)
        if args.process:
            subprocess.call(process_command, shell=True, env=my_env)

    if args.join:
        file_dir = os.path.abspath(os.path.dirname(args.output_file_name))
        os.makedirs(file_dir, exist_ok=True)
        join_all_data(args.output_file_name)

    if args.clean:
        pass
