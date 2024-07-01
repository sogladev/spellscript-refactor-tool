import pytest

from acore_spellscript_refactor.refactor import *

def test_always_passes():
    assert True

@pytest.mark.parametrize('lines, expect',  [
    ([
        'class spell_yogg_saron_malady_of_the_mind : public SpellScriptLoader',
        '{',
        'public:',
        '    spell_yogg_saron_malady_of_the_mind() : SpellScriptLoader("spell_yogg_saron_malady_of_the_mind_something") { }'
        ], 'spell_yogg_saron_malady_of_the_mind_something')
])

def test_find_name_of_script(lines, expect):
    assert find_name_of_script(lines) == expect