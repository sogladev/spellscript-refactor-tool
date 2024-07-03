import argparse

from .refactor import format_first_block_in_file
from .util.logger import logger, set_debug

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file', type=str)
    parser.add_argument('dest_file', nargs='?', type=str, default=None)
    parser.add_argument('--skip', type=int, default=0, help="amount of lines to skip")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--sql_file', type=str, default='script_name_updates.sql')
    args = parser.parse_args()
    if args.verbose:
        set_debug()
    if not args.dest_file:
        args.dest_file = args.source_file
    format_first_block_in_file(args.source_file, args.dest_file, skip=args.skip, sql_path=args.sql_file, create_commit=args.commit)

if __name__ == '__main__':
    main()