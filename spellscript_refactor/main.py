import argparse

from .refactor import format_first_block_in_file
from .util.logger import logger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str)
    parser.add_argument('dest_file', type=str)
    parser.add_argument('--skip', type=int, default=0, help="amount of lines to skip")
    args = parser.parse_args()
    format_first_block_in_file(args.source_file, args.dest_file, skip=args.skip)

if __name__ == '__main__':
    main()