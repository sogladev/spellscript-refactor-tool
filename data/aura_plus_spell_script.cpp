
// 63802 - Brain Link
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
};