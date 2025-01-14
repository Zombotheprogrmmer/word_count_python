import argparse
from os.path import isfile, exists, getsize

def get_details_string(path, details, state):
    output = ""
    if state & 1:
        output += f'{details["lines"]:3} '
    if state & 2:
        output += f'{details["words"]:3} '
    if state & 4:
        output += f'{details["bytes"]:3} '
    if state & 8:
        output += f'{details["chars"]:3} '
    if state & 16:
        output += f'{details["max_length"]:3} '
    if path:
        output += path
    return output

def get_stdin_details():
    from sys import stdin
    details = {
        "lines": 0,
        "words": 0,
        "bytes": 0,
        "chars": 0,
        "max_length": 0
    }
    is_in_word = False
    for line in stdin:
        length = 0
        for char in line:
            details["chars"] += 1
            if not char.isspace():
                is_in_word = True
            elif is_in_word:
                is_in_word = False
                details["words"] += 1
            if char == "\n":
                details["lines"] += 1
            else:
                length += 1
        if is_in_word:
            details["words"] += 1
        if length > details["max_length"]:
            details["max_length"] = length
    return details

def add_to_total(total, details):
    total["lines"] += details["lines"]
    total["words"] += details["words"]
    total["bytes"] += details["bytes"]
    total["chars"] += details["chars"]
    if total["max_length"] < details["max_length"]:
        total["max_length"] = details["max_length"]

def get_file_details(file_path):
    details = {
        "lines": 0,
        "words": 0,
        "bytes": getsize(file_path),
        "chars": 0,
        "max_length": 0
    }
    fh = open(file_path)
    is_in_word = False
    for line in fh:
        length = 0
        for char in line:
            details["chars"] += 1
            if not char.isspace():
                is_in_word = True
            elif is_in_word:
                is_in_word = False
                details["words"] += 1
            if char == "\n":
                details["lines"] += 1
            else:
                length += 1
        if is_in_word:
            details["words"] += 1
        if length > details["max_length"]:
            details["max_length"] = length
    fh.close()
    return details

def get_program_state(args):
    """
    additive state calculator
    1 => lines
    2 => words
    4 => bytes
    8 => chars
    16 => max-length
    """
    state = 0
    if args.lines:
        state |= 1
    if args.words:
        state |= 2
    if args.bytes:
        state |= 4
    if args.chars:
        state |= 8
    if args.max_line_length:
        state |= 16
    # if no flag is passed return 7
    return state if state else 7

def get_path_state(file_path):
    """
    0 path doesn't exist
    1 path is a file
    -1 path is a directory
    """
    if not exists(file_path):
        return 0
    if isfile(file_path):
        return 1
    return -1

def main():
    # create the command line argument parser and add arguments
    parser = argparse.ArgumentParser(
        description="""a recreation of the Unix wc program by Zombotheprogrmmer. 
        Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified. 
        A word is a non-zero-length sequence of printable characters delimited by white space."""
    )
    parser.add_argument("FILE", type=str, nargs="*", help="The adress of file(s) to be proccessed. With no FILE, or when FILE is -, read standard input.")
    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    parser.add_argument("-m", "--chars", action="store_true", help="print the character counts")
    parser.add_argument("-L", "--max-line-length", action="store_true", help="print the maximum display width")
    # parse the arguments
    args = parser.parse_args()

    program_state = get_program_state(args)
    total_details = details = {
        "lines": 0,
        "words": 0,
        "bytes": 0,
        "chars": 0,
        "max_length": 0
    }
    # no FILE provided
    if len(args.FILE) == 0:
        stdin_details = get_stdin_details()
        detail_string = get_details_string("", stdin_details, program_state)
        print(f"\n{detail_string}")
        quit(0)
    # FILE provided
    for path in args.FILE:
        if path == "-":
            stdin_details = get_stdin_details()
            detail_string = get_details_string(path, stdin_details, program_state)
            print(f"\n{detail_string}")
            if len(args.FILE) > 1:
                add_to_total(total_details, stdin_details)
            continue
        path_state = get_path_state(path)
        if path_state == 0:
            print(f"no such file or directory: {file}")
        elif path_state == -1:
            print(f"{file} is a directory")
        else:
            file_details = get_file_details(path)
            if len(args.FILE) > 1:
                add_to_total(total_details, file_details)
            detail_string = get_details_string(path, file_details, program_state)
            print(detail_string)
    if len(args.FILE) > 1:
            total_string = get_details_string("total", total_details, program_state)
            print(total_string)

main()
