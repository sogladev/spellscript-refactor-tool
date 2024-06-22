import pytest

from acore_spellscript_refactor.refactor import *

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

expected_output_spell =\
"""class spell_yogg_saron_brain_link : public SpellScript
{
    PrepareSpellScript(spell_yogg_saron_brain_link);

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
        OnObjectAreaTargetSelect += SpellObjectAreaTargetSelectFn(spell_yogg_saron_brain_link::FilterTargets, EFFECT_0, TARGET_UNIT_SRC_AREA_ENEMY);
    }
};"""

expected_output_aura =\
"""class spell_yogg_saron_brain_link_aura : public AuraScript
{
    PrepareAuraScript(spell_yogg_saron_brain_link_aura);

    bool Validate(SpellInfo const* /*spellInfo*/) override
    {
        return ValidateSpellInfo({ SPELL_BRAIN_LINK_DAMAGE, SPELL_BRAIN_LINK_OK });
    }

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
        OnEffectApply += AuraEffectApplyFn(spell_yogg_saron_brain_link_aura::HandleOnEffectApply, EFFECT_0, SPELL_AURA_PERIODIC_DUMMY, AURA_EFFECT_HANDLE_REAL);
        OnEffectPeriodic += AuraEffectPeriodicFn(spell_yogg_saron_brain_link_aura::OnPeriodic, EFFECT_0, SPELL_AURA_PERIODIC_DUMMY);
    }

protected:
    ObjectGuid _targetGUID;
};"""

expected_out= expected_output_spell +'\n'+expected_output_aura

@pytest.fixture
def lines():
    return input_as_string.split('\n')

@pytest.fixture
def expect() -> str:
    return expected_out

@pytest.fixture
def expect_aura() -> str:
    return expected_output_aura.split('\n')

@pytest.fixture
def expect_spell() -> str:
    return expected_output_spell.split('\n')

@pytest.fixture
def expect_spell_string() -> str:
    return "RegisterSpellAndAuraScriptPair(spell_yogg_saron_brain_link, spell_yogg_saron_brain_link_aura);"

def test_always_passes():
    assert True

def test_find_start_last_index(lines):
    start_index, last_index = find_start_last_index(lines)
    assert start_index == 1
    assert last_index == 100

def test_find_name_of_script(lines):
    assert find_name_of_script(lines) == "spell_yogg_saron_brain_link"

def test_get_script_type(lines):
    start_index, last_index = find_start_last_index(lines)
    assert get_script_type(lines, start_index) == ScriptType.PAIR

def test_find_spell_block_in_pair(lines, expect_spell):
    start_index, last_index = find_start_last_index(lines)
    spell_script_lines = find_spell_block_in_pair(lines[start_index:last_index], ScriptType.SPELL)
    assert len(expect_spell) == len(spell_script_lines)

def test_convert_function_block(lines, expect, expect_spell, expect_aura):
    converted_pair, spell_type, start_index, last_index, _, _ = convert_function_block(lines)
    assert spell_type == ScriptType.PAIR

    spell, aura = converted_pair
    spell, aura = spell.split('\n'), aura.split('\n')

    assert len(expect_spell) == len(spell)
    for i in range(len(aura)):
        assert aura[i] == expect_aura[i], f"{i-1}:\'{aura[i-1]}\'{i}:\'{aura[i]}\'\'{expect_aura[i]}\'"
    assert len(expect_aura) == len(aura)
    assert len(expect_aura) == len(aura)
    for i in range(len(spell)):
        assert spell[i] == expect_spell[i], f"{i-1}:\'{spell[i-1]}\'{i}:\'{spell[i]}\'\'{expect_spell[i]}\'"