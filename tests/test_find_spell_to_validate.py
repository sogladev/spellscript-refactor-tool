import pytest

from spellscript_refactor.refactor import *

def test_always_passes():
    assert True

@pytest.mark.parametrize('line, spell',  [
    ('t->CastSpell(t, SPELL_GRAB_TRIGGERED, true);', 'SPELL_GRAB_TRIGGERED'),
    ('t->CastSpell(t, SPELL_GRAB_TRIGGERED);', 'SPELL_GRAB_TRIGGERED'),
    ('t->CastSpell(t, 6969, true);', '6969'),
    ('t->CastSpell(t, 7171);', '7171'),
    ('me->CastCustomSpell(SPELL_ACTIVATE_CONSTRUCT, SPELLVALUE_MAX_TARGETS, 1, (Unit*)nullptr, false);', 'SPELL_ACTIVATE_CONSTRUCT'),
    ('GetUnitOwner()->ApplySpellImmune(SPELL_DEATH_RAY_DAMAGE_REAL, IMMUNITY_ID, SPELL_DEATH_RAY_DAMAGE_REAL, true);', 'SPELL_DEATH_RAY_DAMAGE_REAL'),


])

def test_find_spell_to_validate(line, spell):
    assert find_spell_to_validate(line) == spell

# def test_replace_new_with_RegisterSpellScript_aura_of_despair():
#     lines_input    = ['    new spell_aura_of_despair();']
#     lines_expected = ['    RegisterSpellScript(spell_aura_of_despair);']
#     lines = replace_new_with_RegisterSpellScript(lines_input, 'spell_aura_of_despair', ScriptType.AURA)
#     assert len(lines) == len(lines_expected)
#     assert lines[0] == lines_expected[0]

def test_format_validate_function():
    spells = ['SPELL_GRAB_TRIGGERED']
    expected = """
    bool Validate(SpellInfo const* /*spellInfo*/) override
    {
        return ValidateSpellInfo({ SPELL_GRAB_TRIGGERED });
    }\n"""
    out = format_validate_function(spells)
    assert out == expected