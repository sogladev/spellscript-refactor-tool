import pytest

from spellscript_refactor.refactor import *

# pytest --pyargs spellscript_refactor
input_as_string =\
"""// 63802 - Brain Link
class spell_yogg_saron_brain_link : public SpellScriptLoader
{
public:
    spell_yogg_saron_brain_link() : SpellScriptLoader("spell_yogg_saron_brain_link") { }

    class spell_yogg_saron_brain_link_AuraScript : public AuraScript
    {
        PrepareAuraScript(spell_yogg_saron_brain_link_AuraScript);

        void HandleOnEffectApply(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
        {
            PreventDefaultAction();
            Player* target = nullptr;
            Map::PlayerList const& pList = GetUnitOwner()->GetMap()->GetPlayers();
            uint8 _offset = urand(0, pList.getSize() - 1);
            uint8 _counter = 0;
            for(Map::PlayerList::const_iterator itr = pList.begin(); itr != pList.end(); ++itr, ++_counter)
            {
                if (itr->GetSource() == GetUnitOwner() || GetUnitOwner()->GetDistance(itr->GetSource()) > 50.0f || !itr->GetSource()->IsAlive() || itr->GetSource()->IsGameMaster())
                    continue;

                if (_counter <= _offset || !target)
                    target = itr->GetSource();
                else
                    break;
            }

            if (!target)
                SetDuration(0);
            else
                _targetGUID = target->GetGUID();
        }

        void OnPeriodic(AuraEffect const*  /*aurEff*/)
        {
            Unit* owner = GetUnitOwner();
            if (!owner)
            {
                SetDuration(0);
                return;
            }

            Unit* _target = ObjectAccessor::GetUnit(*owner, _targetGUID);
            if (!_target || !_target->IsAlive() || std::fabs(owner->GetPositionZ() - _target->GetPositionZ()) > 10.0f) // Target or owner underground
            {
                SetDuration(0);
                return;
            }

            if (owner->GetDistance(_target) > 20.0f)
            {
                owner->CastSpell(_target, SPELL_BRAIN_LINK_DAMAGE, true);
                owner->CastSpell(owner, SPELL_BRAIN_LINK_DAMAGE, true);
            }
            else
                owner->CastSpell(_target, SPELL_BRAIN_LINK_OK, true);
        }

        void Register() override
        {
            OnEffectApply += AuraEffectApplyFn(spell_yogg_saron_brain_link_AuraScript::HandleOnEffectApply, EFFECT_0, SPELL_AURA_PERIODIC_DUMMY, AURA_EFFECT_HANDLE_REAL);
            OnEffectPeriodic += AuraEffectPeriodicFn(spell_yogg_saron_brain_link_AuraScript::OnPeriodic, EFFECT_0, SPELL_AURA_PERIODIC_DUMMY);
        }

    protected:
        ObjectGuid _targetGUID;
    };

    AuraScript* GetAuraScript() const override
    {
        return new spell_yogg_saron_brain_link_AuraScript();
    }

    class spell_yogg_saron_brain_link_SpellScript : public SpellScript
    {
        PrepareSpellScript(spell_yogg_saron_brain_link_SpellScript);

        void FilterTargets(std::list<WorldObject*>& targets)
        {
            std::list<WorldObject*> tempList;
            for (std::list<WorldObject*>::iterator itr = targets.begin(); itr != targets.end(); ++itr)
                if ((*itr)->GetPositionZ() > 300.0f)
                    tempList.push_back(*itr);

            targets.clear();
            for (std::list<WorldObject*>::iterator itr = tempList.begin(); itr != tempList.end(); ++itr)
                targets.push_back(*itr);
        }

        void Register() override
        {
            OnObjectAreaTargetSelect += SpellObjectAreaTargetSelectFn(spell_yogg_saron_brain_link_SpellScript::FilterTargets, EFFECT_0, TARGET_UNIT_SRC_AREA_ENEMY);
        }
    };

    SpellScript* GetSpellScript() const override
    {
        return new spell_yogg_saron_brain_link_SpellScript();
    }
};"""

expected_output =\
"""class spell_yogg_saron_grim_reprisal_aura : public AuraScript
{
    PrepareAuraScript(spell_yogg_saron_grim_reprisal_aura);

    bool Validate(SpellInfo const* /*spellInfo*/) override
    {
        return ValidateSpellInfo({ SPELL_GRIM_REPRISAL_DAMAGE });
    }

    void HandleProc(AuraEffect const* aurEff, ProcEventInfo& eventInfo)
    {
        DamageInfo* damageInfo = eventInfo.GetDamageInfo();

        if (!damageInfo || !damageInfo->GetDamage())
        {
            return;
        }

        int32 damage = CalculatePct(static_cast<int32>(damageInfo->GetDamage()), 60);
        GetTarget()->CastCustomSpell(SPELL_GRIM_REPRISAL_DAMAGE, SPELLVALUE_BASE_POINT0, damage, damageInfo->GetAttacker(), true, nullptr, aurEff);
    }

    void Register() override
    {
        OnEffectProc += AuraEffectProcFn(spell_yogg_saron_grim_reprisal_aura::HandleProc, EFFECT_0, SPELL_AURA_DUMMY);
    }
};"""

@pytest.fixture
def lines():
    return input_as_string.split('\n')

@pytest.fixture
def expect() -> str:
    return expected_output

@pytest.fixture
def expect_spell_string() -> str:
    return "RegisterSpellScript(spell_yogg_saron_grim_reprisal_aura);"

def test_always_passes():
    assert True

def test_find_start_last_index(lines):
    start_index, last_index = find_start_last_index(lines)
    assert start_index == 1
    assert last_index == 38

def test_find_name_of_script(lines):
    assert find_name_of_script(lines) == "spell_yogg_saron_grim_reprisal"

def test_is_aura_script(lines):
    assert is_aura_script(lines) == True

def test_find_register_start_end_index(lines):
    start_index, last_index = find_start_last_index(lines)
    register_start_index, register_end_index = find_register_start_end_index(lines, start_index)
    assert lines[register_start_index].lstrip() == "void Register() override"
    assert register_end_index == register_start_index + 3
    assert lines[register_end_index] == "        }"

def test_find_register_statements(lines):
    register_statements = find_register_statements(lines, 1)
    assert len(register_statements) == 1
    assert register_statements[0] == "            OnEffectProc += AuraEffectProcFn(spell_yogg_saron_grim_reprisal_AuraScript::HandleProc, EFFECT_0, SPELL_AURA_DUMMY);"

def test_format_register_statements():
    register_statements = ["            OnEffectProc += AuraEffectProcFn(spell_yogg_saron_grim_reprisal_AuraScript::HandleProc, EFFECT_0, SPELL_AURA_DUMMY);"]
    formatted_statements = format_register_statements(register_statements)
    assert len(formatted_statements) == 1
    assert formatted_statements[0] == "        OnEffectProc += AuraEffectProcFn(spell_yogg_saron_grim_reprisal_aura::HandleProc, EFFECT_0, SPELL_AURA_DUMMY);"

def test_find_content_start_end_index(lines):
    content_index_start, content_index_end = find_content_start_end_index(lines)
    assert lines[content_index_start].lstrip() == "PrepareAuraScript(spell_yogg_saron_grim_reprisal_AuraScript);"
    assert lines[content_index_end].lstrip() == "void Register() override"

def test_format_content_start_end_index(lines):
    content_index_start, content_index_end = find_content_start_end_index(lines)
    content_statements = lines[content_index_start+1:content_index_end]
    formatted_content_statements = format_content_statements(content_statements);
    assert len(formatted_content_statements) == 19
    assert formatted_content_statements[1] == "    bool Validate(SpellInfo const* /*spellInfo*/) override"
    assert formatted_content_statements[2] == "    {"
    assert formatted_content_statements[3] == "        return ValidateSpellInfo({ SPELL_GRIM_REPRISAL_DAMAGE });"
    assert all(f.strip() != '' or (f.strip() == '' and f == '') for f in formatted_content_statements)

def test_convert_function_block(lines, expect, expect_spell_string):
    out, spell_string, start_index, last_index, _ = convert_function_block(lines)
    assert spell_string.lstrip() == expect_spell_string
    assert start_index == 1
    assert last_index == 38
    assert expect == out
    out = out.split('\n')
    expect = expect.split('\n')
    assert len(expect) == len(out)
    for i in range(len(out)):
        assert out[i] == expect[i], f"{i-1}:\'{out[i-1]}\'{i}:\'{out[i]}\'\'{expect[i]}\'"

