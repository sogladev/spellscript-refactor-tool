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
    lines_input    = ['void AddSC_', '    new spell_aura_of_despair();']
    lines_expected = ['void AddSC_', '    RegisterSpellScript(spell_aura_of_despair);']
    lines, _ = replace_new_with_RegisterSpellScript(lines_input, 'spell_aura_of_despair', ScriptType.AURA)
    assert len(lines) == len(lines_expected)
    assert lines[1] == lines_expected[1]


def test_replace_new_with_RegisterSpellScript_hadronox():
    lines_input = [
        'void AddSC_',
        '    new spell_hadronox_summon_periodic("spell_hadronox_summon_periodic_necromancer", 10000, SPELL_SUMMON_ANUBAR_NECROMANCER);',
        '    new spell_hadronox_summon_periodic("spell_hadronox_summon_periodic_crypt_fiend", 5000, SPELL_SUMMON_ANUBAR_CRYPT_FIEND);'
    ]
    lines_expected = [
        'void AddSC_',
        '    RegisterSpellScriptWithArgs(spell_hadronox_summon_periodic_aura, "spell_hadronox_summon_periodic_necromancer_aura", 10000, SPELL_SUMMON_ANUBAR_NECROMANCER);',
        '    RegisterSpellScriptWithArgs(spell_hadronox_summon_periodic_aura, "spell_hadronox_summon_periodic_crypt_fiend_aura", 5000, SPELL_SUMMON_ANUBAR_CRYPT_FIEND);'
    ]

    lines, _ = replace_new_with_RegisterSpellScript(lines_input, 'spell_hadronox_summon_periodic_aura', ScriptType.AURA)
    assert lines[1] == lines_expected[1]
    assert lines[2] == lines_expected[2]
    assert len(lines) == len(lines_expected)