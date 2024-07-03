import argparse
from pathlib import Path

from .refactor import format_first_block_in_file
from .util.logger import logger, set_debug

def discover():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip', type=int, default=0, help="amount of lines to skip")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--recursive', action='store_true')
    parser.add_argument('--sql_file', type=str, default='script_name_updates.sql')
    args = parser.parse_args()
    if args.verbose:
        set_debug()
    cwd = Path(".")
    if args.recursive:
        cpp_files = cwd.glob("**/*cpp")
    else:
        cpp_files = cwd.glob("*cpp")
    for cpp in list(cpp_files):
        source_file = cpp.absolute()
        dest_file = source_file
        for _ in range(100):
            try:
                format_first_block_in_file(source_file, dest_file, skip=0, sql_path=args.sql_file, create_commit=args.commit)
            except ValueError:
                break

if __name__ == '__main__':
    discover()