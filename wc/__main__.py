import argparse

def main():
    # create the command line argument parser and add arguments
    parser = argparse.ArgumentParser(description="a recreation of the Unix wc program by Zombotheprogrmmer. Print newline, word, and byte counts for each FILE, and a total line if more than one FILE is specified. A word is a non-zero-length sequence of printable characters delimited by white space.")
    parser.add_argument("FILE", type=str, nargs="*", help="The adress of file(s) to be proccessed. With no FILE, or when FILE is -, read standard input.")
    
    # parse the arguments
    args = parser.parse_args()

main()
