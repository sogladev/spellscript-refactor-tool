import pytest

from acore_spellscript_refactor.refactor import *

def test_always_passes():
    assert True

@pytest.mark.parametrize('line, spells',  [
    ('me->CastSpell(me, RAID_MODE(SPELL_TRAITOR_KING_10, SPELL_TRAITOR_KING_25, SPELL_TRAITOR_KING_10, SPELL_TRAITOR_KING_25), true);', ['SPELL_TRAITOR_KING_10', 'SPELL_TRAITOR_KING_25']),
    ('t->CastSpell(t, SPELL_GRAB_TRIGGERED, true);', [ 'SPELL_GRAB_TRIGGERED']),
    ('t->CastSpell(t, SPELL_GRAB_TRIGGERED);', [ 'SPELL_GRAB_TRIGGERED']),
    ('t->CastSpell(t, 6969, true);', [ '6969']),
    ('t->CastSpell(t, 7171);', [ '7171']),
    ('me->CastCustomSpell(SPELL_ACTIVATE_CONSTRUCT, SPELLVALUE_MAX_TARGETS, 1, (Unit*)nullptr, false);', [ 'SPELL_ACTIVATE_CONSTRUCT']),
    ('GetUnitOwner()->ApplySpellImmune(SPELL_DEATH_RAY_DAMAGE_REAL, IMMUNITY_ID, SPELL_DEATH_RAY_DAMAGE_REAL, true);', [ 'SPELL_DEATH_RAY_DAMAGE_REAL']),
    ('GetUnitOwner()->ApplySpellImmune(SPELL_DEATH_RAY_DAMAGE_REAL, IMMUNITY_ID, SPELL_DEATH_RAY_DAMAGE_REAL, true);', [ 'SPELL_DEATH_RAY_DAMAGE_REAL']),
    ('target->CastCustomSpell(dmgInfo.GetAttacker(), SPELL_REFLECTIVE_SHIELD_T, &bp, nullptr, nullptr, true, nullptr, aurEff);', [ 'SPELL_REFLECTIVE_SHIELD_T']),
    ('target->CastCustomSpell(dmgInfo.GetAttacker(), 717878, &bp, nullptr, nullptr, true, nullptr, aurEff);', [ '717878']),
    ('target->CastCustomSpell(dmgInfo.G7etAttacker(), 717878, &2bp, nullptr, nullptr, true, nullptr, aurEff);', [ '717878']),
    ('GetUnitOwner()->CastSpell(target, GetSpellInfo()->Effects[effect->GetEffIndex()].TriggerSpell, true);', []),
    ('GetCaster()->CastSpell(GetHitUnit(), (*i)->GetAmount(), true);', []),
    ('GetCaster()->CastSpell(target, GetEffectValue(), true);', []),
    ('GetCaster()->CastSpell(target, GetEffectValue(), true);', []),
    ('GetUnitOwner()->CastSpell(GetUnitOwner(), RAND(SPELL_SINFUL_PERIODIC, SPELL_SINISTER_PERIODIC, SPELL_VILE_PERIODIC, SPELL_WICKED_PERIODIC), true);', ['SPELL_SINFUL_PERIODIC', 'SPELL_SINISTER_PERIODIC', 'SPELL_VILE_PERIODIC', 'SPELL_WICKED_PERIODIC']),
    ('(player->GetAuraCount(SPELL_OSCILLATION_FIELD) == 5 && player->GetQuestStatus(QUEST_GAUGING_THE_RESONANT_FREQUENCY) == QUEST_STATUS_INCOMPLETE)', ['SPELL_OSCILLATION_FIELD']),
])

def test_find_spell_to_validate(line, spells):
    found_spells = find_spells_to_validate(line)
    assert all(f in spells for f in found_spells)
    assert len(found_spells) == len(spells)

def test_format_validate_function():
    spells = ['SPELL_GRAB_TRIGGERED']
    expected = """
    bool Validate(SpellInfo const* /*spellInfo*/) override
    {
        return ValidateSpellInfo({ SPELL_GRAB_TRIGGERED });
    }\n"""
    out = format_validate_function(spells)
    assert out == expected
