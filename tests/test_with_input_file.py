import pytest

from acore_spellscript_refactor.refactor import *

FILENAME = "tests/test_with_input_file/boss_yoggsaron.cpp"

@pytest.fixture
def lines():
    with open(FILENAME, 'r') as file:
        lines = file.read();
        return lines.split('\n')

@pytest.fixture
def expect() -> str:
    return expected_output

@pytest.fixture
def expect_spell_string() -> str:
    return "RegisterSpellScript(spell_yogg_saron_malady_of_the_mind_aura);"

expected_output =\
"""class spell_yogg_saron_malady_of_the_mind_aura : public AuraScript
{
    PrepareAuraScript(spell_yogg_saron_malady_of_the_mind_aura);

    bool Validate(SpellInfo const* /*spellInfo*/) override
    {
        return ValidateSpellInfo({ SPELL_DEATH_RAY_DAMAGE_REAL, SPELL_MALADY_OF_THE_MIND_TRIGGER });
    }

    void OnApply(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        GetUnitOwner()->ApplySpellImmune(SPELL_DEATH_RAY_DAMAGE_REAL, IMMUNITY_ID, SPELL_DEATH_RAY_DAMAGE_REAL, true);
    }

    void OnRemove(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        GetUnitOwner()->ApplySpellImmune(SPELL_DEATH_RAY_DAMAGE_REAL, IMMUNITY_ID, SPELL_DEATH_RAY_DAMAGE_REAL, false);
        GetUnitOwner()->CastCustomSpell(SPELL_MALADY_OF_THE_MIND_TRIGGER, SPELLVALUE_MAX_TARGETS, 1, GetUnitOwner(), true);
    }

    void Register() override
    {
        OnEffectApply += AuraEffectApplyFn(spell_yogg_saron_malady_of_the_mind_aura::OnApply, EFFECT_1, SPELL_AURA_MOD_FEAR, AURA_EFFECT_HANDLE_REAL);
        OnEffectRemove += AuraEffectRemoveFn(spell_yogg_saron_malady_of_the_mind_aura::OnRemove, EFFECT_1, SPELL_AURA_MOD_FEAR, AURA_EFFECT_HANDLE_REAL);
    }
};"""

def test_always_passes():
    assert True

def test_find_start_last_index(lines):
    start_index, last_index = find_start_last_index(lines)
    assert start_index == 2234, lines[start_index]
    assert last_index == 2265

def test_find_name_of_script(lines):
    start_index, last_index = find_start_last_index(lines)
    assert find_name_of_script(lines, start_index) == "spell_yogg_saron_malady_of_the_mind"

def test_get_script_type(lines):
    start_index, last_index = find_start_last_index(lines)
    assert get_script_type(lines, start_index) == ScriptType.AURA

def test_find_register_start_end_index(lines):
    start_index, last_index = find_start_last_index(lines)
    register_start_index, register_end_index = find_register_start_end_index(lines, start_index)
    assert lines[register_start_index].lstrip() == "void Register() override"
    assert register_end_index == register_start_index + 4
    assert lines[register_end_index] == "        }"

def test_find_register_statements(lines):
    register_statements = find_register_statements(lines, 1)
    assert len(register_statements) == 2
    assert register_statements[0] == "            OnEffectApply += AuraEffectApplyFn(spell_yogg_saron_malady_of_the_mind_AuraScript::OnApply, EFFECT_1, SPELL_AURA_MOD_FEAR, AURA_EFFECT_HANDLE_REAL);"

def test_format_register_statements():
    register_statements = ["            OnEffectProc += AuraEffectProcFn(spell_yogg_saron_grim_reprisal_AuraScript::HandleProc, EFFECT_0, SPELL_AURA_DUMMY);"]
    formatted_statements = format_register_statements(register_statements)
    assert len(formatted_statements) == 1
    assert formatted_statements[0] == "        OnEffectProc += AuraEffectProcFn(spell_yogg_saron_grim_reprisal_aura::HandleProc, EFFECT_0, SPELL_AURA_DUMMY);"

def test_find_content_start_end_index(lines):
    start_index, last_index = find_start_last_index(lines)
    content_index_start, content_index_end = find_content_start_end_index(lines, start_index)
    assert lines[content_index_start].lstrip() == "PrepareAuraScript(spell_yogg_saron_malady_of_the_mind_AuraScript);"
    assert lines[content_index_end].lstrip() == "void Register() override"

def test_format_content_start_end_index(lines):
    content_index_start, content_index_end = find_content_start_end_index(lines)
    content_statements = lines[content_index_start+1:content_index_end]
    formatted_content_statements = format_content_statements(content_statements);
    assert len(formatted_content_statements) == 12
    assert formatted_content_statements[1] == "    void OnApply(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)"
    assert formatted_content_statements[2] == "    {"
    assert all(f.strip() != '' or (f.strip() == '' and f == '') for f in formatted_content_statements)

def test_convert_function_block(lines, expect, expect_spell_string):
    out, spell_type, start_index, last_index, _, _ = convert_function_block(lines)
    assert spell_type == ScriptType.AURA
    assert last_index - start_index == 31
    assert expect == out
    out = out.split('\n')
    expect = expect.split('\n')
    assert len(expect) == len(out)
    for i in range(len(out)):
        assert out[i] == expect[i], f"{i-1}:\'{out[i-1]}\'{i}:\'{out[i]}\'\'{expect[i]}\'"
