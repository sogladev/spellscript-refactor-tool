
// 64172 - Titanic Storm
class spell_yogg_saron_titanic_storm : public SpellScriptLoader
{
public:
    spell_yogg_saron_titanic_storm() : SpellScriptLoader("spell_yogg_saron_titanic_storm") { }

    class spell_yogg_saron_titanic_storm_SpellScript : public SpellScript
    {
        PrepareSpellScript(spell_yogg_saron_titanic_storm_SpellScript);

        void HandleDummyEffect(SpellEffIndex effIndex)
        {
            PreventHitDefaultEffect(effIndex);
            if (Unit* target = GetHitUnit())
                Unit::Kill(GetCaster(), target);
        }

        void FilterTargets(std::list<WorldObject*>& targets)
        {
            WorldObject* target = nullptr;
            for (std::list<WorldObject*>::iterator itr = targets.begin(); itr != targets.end(); ++itr)
                if ((*itr)->ToUnit()->HasAura(SPELL_WEAKENED))
                {
                    target = *itr;
                    break;
                }

            targets.clear();
            if (target)
                targets.push_back(target);
        }

        void Register() override
        {
            OnEffectHitTarget += SpellEffectFn(spell_yogg_saron_titanic_storm_SpellScript::HandleDummyEffect, EFFECT_0, SPELL_EFFECT_DUMMY);
            OnObjectAreaTargetSelect += SpellObjectAreaTargetSelectFn(spell_yogg_saron_titanic_storm_SpellScript::FilterTargets, EFFECT_0, TARGET_UNIT_SRC_AREA_ENTRY);
        }
    };

    SpellScript* GetSpellScript() const override
    {
        return new spell_yogg_saron_titanic_storm_SpellScript();
    }
};

void AddSC_
    new spell_yogg_saron_titanic_storm();