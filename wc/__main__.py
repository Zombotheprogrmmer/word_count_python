import argparse
from os.path import isfile, exists

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
    
    # parse the arguments
    args = parser.parse_args()
    for file in args.FILE:
        state = get_path_state(file)
        if state == 0:
            print(f"no such file or directory: {file}")
        elif state == -1:
            print(f"{file} is a directory")
        else:
            pass

main()
