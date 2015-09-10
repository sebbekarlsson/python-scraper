import sys, getopt
from parser import Parser
import yaml

def main():
    url = sys.argv[1]

    parser = Parser(url, yaml.load_all(open('config.yaml', 'r')))

    parser.run()

if (__name__) == '__main__':
    main()
