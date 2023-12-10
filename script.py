import argparse
import logging
import os
import sys
import textwrap
from functools import partial
from pathlib import Path

import cli_functions
import config
from data_cleaner.data_extractor import get_handler, Handler
from data_cleaner.data_validator import get_validated_records, get_validated_dataset
from domain.models import PersonUser

FORMAT = '%(asctime)s - %(levelname)-8s - %(module)-20s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    filename='data_cleaning_logs.log',
    encoding='utf-8'
)


def get_files(dir_path):
    for dirpath, _, filenames in os.walk(dir_path):
        for filename in filenames:
            yield Path(dirpath) / filename


def extract_data(handler: Handler, dir_path: Path) -> list[PersonUser]:
    for file in get_files(dir_path):
        handler.handle(file)

    return handler.get_data()


def get_data(handler: Handler, dir_path: Path):
    unvalidated_data = extract_data(handler, dir_path)
    validated_records = get_validated_records(unvalidated_data)
    return get_validated_dataset(validated_records)


def convert_to_underscores(s):
    return s.replace('-', '_')


def main():
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--login', default="")
    parent.add_argument('--password', default="")

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Welcome! If you launch this program for the first time, please run:
            python script.py create-database
        ---------------------------------------------------------------------------
        The commands should be run as follows:
            python script.py print-children --login mylogin --password '@mypassword'
        Please mind that the password should be put within SINGLE QUOTES
        ---------------------------------------------------------------------------
        The available commands are listed and explained below.
        ---------------------------------------------------------------------------
        Please mind that some commands are available for ADMIN users only. 
        If you try to run one of these commands without ADMIN credentials, 
        you will see the following message: 
        You are not authorized to perform this action (admin account required).
        ---------------------------------------------------------------------------
        '''))
    subparsers = parser.add_subparsers()

    parsers = []

    commands = [
        'print-all-accounts',
        'print-oldest-account',
        'group-by-age',
        'print-children',
        'find-similar-children-by-age',
    ]
    help_messages = [
        "Displays the total number of valid \naccounts (only for ADMIN users).",
        "Displays information about the account with the longest existence (only for ADMIN users).",
        "Groups children by age and displays relevant information (only for ADMIN users).",
        "Displays information about your children.",
        "Displays users with children of the same age as at least one of your children."
    ]

    for command, help_message in zip(commands, help_messages):
        p = subparsers.add_parser(command, parents=[parent], help=help_message)
        function = getattr(cli_functions, convert_to_underscores(command))
        p.set_defaults(func=function)
        parsers.append(p)

    p = subparsers.add_parser('create-database', help="Create a SQL database.")
    function = getattr(cli_functions, 'create_database')
    data = get_data(handler=get_handler(), dir_path=config.RAW_DATA_PATH)
    p.set_defaults(func=partial(function, data=data))
    parsers.append(p)

    if sys.argv[-1] == '--password':
        print("Please provide your password in SINGLE QUOTES, for example:\n"
              "python script.py print-children --login 123456789 --password '$mypassword@'")
        sys.exit(1)
    elif len(sys.argv) == 1:
        print("Please run 'python script.py --help' to see the description.")
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
