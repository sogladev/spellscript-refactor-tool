
// 63830, 63881 - Malady of the Mind
class spell_yogg_saron_malady_of_the_mind_aura : public AuraScript
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
};

void AddSC_
    RegisterSpellScript(spell_yogg_saron_malady_of_the_mind_aura);