import pytest

from acore_spellscript_refactor.refactor import *

def test_always_passes():
    assert True

@pytest.mark.parametrize('lines, expect',  [
    (['class spell_halion_combustion_consumption : public SpellScriptLoader'], 'spell_halion_combustion_consumption'),
    (['class spell_q11515_fel_siphon_dummy : public SpellScriptLoader'], 'spell_q11515_fel_siphon_dummy'),
    (['class spell_q10929_fumping : SpellScriptLoader'], 'spell_q10929_fumping'),
])

def test_find_name_of_script(lines, expect):
    assert find_name_of_script(lines) == expect