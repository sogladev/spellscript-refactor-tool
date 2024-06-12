import pytest

from acore_spellscript_refactor.refactor import *

def test_always_passes():
    assert True

@pytest.mark.parametrize('spell_script, spell_script_without_suffix',  [
    ('spell_aura_of_despair', 'spell_aura_of_despair'),
    ('spell_aura_of_despair_aura', 'spell_aura_of_despair'),
    ('spell_aura_of_despair_spell', 'spell_aura_of_despair'),
])

def test_remove_aura_spell_suffix(spell_script, spell_script_without_suffix):
    assert remove_aura_spell_suffix(spell_script) == spell_script_without_suffix

def test_replace_new_with_RegisterSpellScript_aura_of_despair():
    lines_input    = ['    new spell_aura_of_despair();']
    lines_expected = ['    RegisterSpellScript(spell_aura_of_despair);']
    lines = replace_new_with_RegisterSpellScript(lines_input, 'spell_aura_of_despair', ScriptType.AURA)
    assert len(lines) == len(lines_expected)
    assert lines[0] == lines_expected[0]