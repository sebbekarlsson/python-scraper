import sys, getopt
from parser import Parser

def main():
    url = sys.argv[1]
    parser = Parser(url)

    parser.run()

if (__name__) == '__main__':
    main()