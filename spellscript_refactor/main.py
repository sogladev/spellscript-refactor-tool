import argparse

from .refactor import format_first_block_in_file
from .util.logger import logger
from .util.colors import color, Color

def main():
    logger.info("Program started")
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str)
    parser.add_argument('dest_file', type=str)
    args = parser.parse_args()
    format_first_block_in_file(args.source_file, args.dest_file)

if __name__ == '__main__':
    main()