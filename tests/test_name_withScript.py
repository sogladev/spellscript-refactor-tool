import pytest

from acore_spellscript_refactor.refactor import *

# pytest --pyargs spellscript_refactor
input_as_string =\
"""
class spell_the_eye_countercharge : public SpellScriptLoader
{
public:
    spell_the_eye_countercharge() : SpellScriptLoader("spell_the_eye_countercharge") { }

    class spell_the_eye_counterchargeScript : public AuraScript
    {
        PrepareAuraScript(spell_the_eye_counterchargeScript);

        bool PrepareProc(ProcEventInfo&  /*eventInfo*/)
        {
            // xinef: prevent charge drop
            PreventDefaultAction();
            return true;
        }

        void Register() override
        {
            DoCheckProc += AuraCheckProcFn(spell_the_eye_counterchargeScript::PrepareProc);
        }
    };

    AuraScript* GetAuraScript() const override
    {
        return new spell_the_eye_counterchargeScript();
    }
};"""

expected_output =\
"""class spell_the_eye_countercharge_aura : public AuraScript
{
    PrepareAuraScript(spell_the_eye_countercharge_aura);

    bool PrepareProc(ProcEventInfo&  /*eventInfo*/)
    {
        // xinef: prevent charge drop
        PreventDefaultAction();
        return true;
    }

    void Register() override
    {
        DoCheckProc += AuraCheckProcFn(spell_the_eye_countercharge_aura::PrepareProc);
    }
};"""


@pytest.fixture
def lines():
    return input_as_string.split('\n')

@pytest.fixture
def expect() -> str:
    return expected_output

def test_always_passes():
    assert True

def test_convert_function_block(lines, expect):
    out, _, _, _, _, _ = convert_function_block(lines)
    out = out.split('\n')
    expect = expect.split('\n')
    for i in range(len(out)):
        assert out[i] == expect[i]
    assert len(expect) == len(out)
    assert expect == out

