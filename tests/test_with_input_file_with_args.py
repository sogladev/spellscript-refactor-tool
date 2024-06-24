import pytest
import os

from acore_spellscript_refactor.refactor import *

ENV_GITHUB_CI = "CI"

FILENAME_READ = "tests/test_with_input_file_with_args/boss_hadronox_read.cpp"
FILENAME_WRITE = "tests/test_with_input_file_with_args/boss_hadronox_write.cpp"
FILENAME_EXPECTED = "tests/test_with_input_file_with_args/boss_hadronox_expected.cpp"

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

def test_format_content_statement():
    input = 'spell_hadronox_summon_periodic_aura(const char* name, uint32 delay, uint32 spellEntry) : SpellScriptLoader(name), _delay(delay), _spellEntry(spellEntry) { }'
    expected = 'spell_hadronox_summon_periodic_aura(uint32 delay, uint32 spellEntry) : _delay(delay), _spellEntry(spellEntry) { }'
    out = format_content_statement(input)
    assert out == expected
