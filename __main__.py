import sys, getopt
from parser import Parser
import yaml

def main():
    url = sys.argv[1]

    config = yaml.load_all(open('config.yaml', 'r'))
    parser = Parser(url, config)

    parser.run()

if (__name__) == '__main__':
    main()