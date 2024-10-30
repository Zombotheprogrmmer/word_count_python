import argparse
from os.path import isfile, exists

def get_details_string(path, details, state):
    output = ""
    if state & 1:
        output += f'{details["lines"]:3} '
    if state & 2:
        output += f'{details["words"]:3} '
    if path:
        output += path
    return output

def get_file_details(file_path):
    details = {
        "lines": 0,
        "words": 0,
    }
    fh = open(file_path)
    is_in_word = False
    for line in fh:
        for char in line:
            if not char.isspace():
                is_in_word = True
            elif is_in_word:
                is_in_word = False
                details["words"] += 1
            if char == "\n":
                details["lines"] += 1
    fh.close()
    return details

def get_program_state(args):
    """
    additive state calculator
    1 => lines
    2 => words
    """
    state = 0
    if args.lines:
        state |= 1
    if args.words:
        state |= 2
    return state

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
    parser = argparse.ArgumentParser(description="a recreation of the Unix wc program by Zombotheprogrmmer. Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified. A word is a non-zero-length sequence of printable characters delimited by white space.")
    parser.add_argument("FILE", type=str, nargs="*", help="The adress of file(s) to be proccessed. With no FILE, or when FILE is -, read standard input.")
    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    # parse the arguments
    args = parser.parse_args()
    program_state = get_program_state(args)
    for path in args.FILE:
        path_state = get_path_state(path)
        if path_state == 0:
            print(f"no such file or directory: {file}")
        elif path_state == -1:
            print(f"{file} is a directory")
        else:
            file_details = get_file_details(path)
            detail_string = get_details_string(path, file_details, program_state)
            print(detail_string)

main()
