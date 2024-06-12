import pytest

from acore_spellscript_refactor.refactor import *

FILENAME_READ = "tests/test_write_replace_file/boss_yoggsaron_read.cpp"
FILENAME_WRITE = "tests/test_write_replace_file/boss_yoggsaron_write.cpp"
FILENAME_EXPECTED = "tests/test_write_replace_file/boss_yoggsaron_expected.cpp"

@pytest.fixture
def expect():
    with open(FILENAME_EXPECTED, 'r') as file:
        lines = file.read();
        return lines.split('\n')

def test_always_passes():
    assert True

def test_format_first_block_in_file(expect):
    format_first_block_in_file(FILENAME_READ, FILENAME_WRITE)

    with open(FILENAME_WRITE, 'r') as file:
        lines = file.read();
        lines = lines.split('\n')

    for i in range(len(lines)):
        assert lines[i] == expect[i], f"\'{i}:\'{lines[i]}\'\'{expect[i]}\'"
    assert len(lines) == len(expect)
