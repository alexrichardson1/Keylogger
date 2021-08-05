#!/usr/bin/python3

import sys
import re
from colorama import Fore, Back, Style


def exit_failure(error_message):
    print(Fore.RED + Style.BRIGHT + "fatal: " + error_message + Style.RESET_ALL)
    print("-------------------------------")
    sys.exit(1)


def follows_convention(first_line):
    # located in the README
    types = ["feat", "fix", "style", "refactor",
             "perf", "test", "docs", "chore", "build", "ci"]
    if all([re.match(t + "(\S+): ", first_line) == None for t in types]):
        exit_failure("commit message does not follow convention.")
    if len(first_line) > 50:
        exit_failure("header is longer than 50 characters.")


def read_commit_msg(file):
    new_commit_message = []
    with open(file, "r") as fp:
        lines = fp.readlines()
        follows_convention(lines[0])
    fp.close()
    return new_commit_message


def main():
    print("--- Running commit-msg hook ---")
    file = sys.argv[1]
    read_commit_msg(file)
    print(Fore.GREEN + Style.BRIGHT +
          "commit-msg hook finished successfully." + Style.RESET_ALL)
    print("-------------------------------")
    sys.exit(0)


if __name__ == "__main__":
    main()
