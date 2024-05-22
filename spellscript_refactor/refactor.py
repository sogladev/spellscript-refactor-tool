import re

from .util.colors import Color, color

def find_start_last_index(lines_to_search):
    start_index = None
    for i, line in enumerate(lines_to_search):
        if (start_index is None and re.match("class .* : public SpellScriptLoader", line)):
            print(i, line)
            start_index = i
        if start_index:
            if line.rstrip() == '};':
                return start_index, i
    print(color(f"ERROR: No spells scripts found", Color.RED))

def find_name_of_script(lines_to_search, start_index=0):
    for line in lines_to_search[start_index:]:
        if '"' in line:
            name = re.findall(r'"(.*?)"', line)[0]
            return name

def is_aura_script(lines_to_search):
    for line in lines_to_search:
        if "AuraScript" in line:
            print(color("AuraScript", Color.GREEN))
            return False
        if "SpellScript" in line:
            print(color("SpellScript", Color.GREEN))
            return True

def find_register_start_end_index(lines_to_search, start_index=0):
    start = None
    for i, line in enumerate(lines_to_search[start_index:]):
        if 'void Register' in line:
           start = i
        if start:
            if line.strip() == '}':
                return start+start_index, i+start_index

def find_register_statements(lines, start_index):
    register_index_start, register_index_bracket = find_register_start_end_index(lines[start_index:])
    register_index_start += start_index
    register_index_bracket += start_index
    register_statements = lines[register_index_start+2:register_index_bracket]
    return register_statements

def format_register_statements(register_statements):
    register_statements_format = []
    for c in register_statements:
        if c.strip() == '':
            c = ''
        else:
            c = 8*' ' + c.lstrip()
            c = c.replace('_AuraScript','_aura')
            c = c.replace('_SpellScript','')
        register_statements_format.append(c)
    return register_statements_format

def find_content_start_end_index(lines_to_search, start_index=0):
    start = None
    for i, line in enumerate(lines_to_search[start_index:]):
        if "Prepare" in line:
            start = i
        if start:
            if 'void Register' in line:
                return start+start_index, i+start_index

def find_content_statements(lines, start_index):
    content_index_start, content_index_end = find_content_start_end_index(lines[start_index:])
    content_index_start += start_index
    content_index_end += start_index
    content_statements = lines[content_index_start+1:content_index_end]
    return content_statements

def format_content_statements(content_statements):
    content_statements_format = []
    for c in content_statements:
        if c.strip() == '':
            c = ''
        elif 8*' ' in c:
            c = (4*' ').join(c.split(4*' ')[1:])
        c = c.replace('_AuraScript','_aura')
        c = c.replace('_SpellScript','')
        content_statements_format.append(c)
    return content_statements_format

def convert_function_block(lines) -> tuple[str, str, int, int, str]:
    start_index, last_index = find_start_last_index(lines)
    isSpellScript = not is_aura_script(lines[start_index:])
    type: str = 'SpellScript' if isSpellScript else 'AuraScript'
    prepare: str = 'Spell' if isSpellScript else 'Aura'
    script_name = find_name_of_script(lines[start_index:]) + ('' if isSpellScript else '_aura')
    register_statements = find_register_statements(lines, start_index)
    register_statements = format_register_statements(register_statements)
    content_statements = find_content_statements(lines, start_index)
    content_statements = format_content_statements(content_statements)
    register_spellstring = f"RegisterSpellScript({script_name});"
    content: str = '\n'.join(content_statements)
    register_formatted: str = '\n'.join(register_statements)
    out_formatted = \
"""class """+script_name+""" : public """+type+"""\n{
    Prepare"""+prepare+"""Script("""+script_name+");\n"\
+content+\
"""
    void Register() override
    {\n"""+\
register_formatted+\
"""
    }
};\n"""
    register_spellstring = f"RegisterSpellScript({script_name});"
    return out_formatted, register_spellstring, start_index, last_index, script_name

OFFSET = 0
FILENAME = "/home/jelle/wd/wow/azerothcore-wotlk/src/server/scripts/Northrend/Ulduar/Ulduar/boss_yoggsaron.cpp"

input =\
"""
class spell_yogg_saron_malady_of_the_mind : public SpellScriptLoader
{
public:
    spell_yogg_saron_malady_of_the_mind() : SpellScriptLoader("spell_yogg_saron_malady_of_the_mind") { }

    class spell_yogg_saron_malady_of_the_mind_AuraScript : public AuraScript
    {
        PrepareAuraScript(spell_yogg_saron_malady_of_the_mind_AuraScript);

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
            OnEffectApply += AuraEffectApplyFn(spell_yogg_saron_malady_of_the_mind_AuraScript::OnApply, EFFECT_1, SPELL_AURA_MOD_FEAR, AURA_EFFECT_HANDLE_REAL);
            OnEffectRemove += AuraEffectRemoveFn(spell_yogg_saron_malady_of_the_mind_AuraScript::OnRemove, EFFECT_1, SPELL_AURA_MOD_FEAR, AURA_EFFECT_HANDLE_REAL);
        }
    };

    AuraScript* GetAuraScript() const override
    {
        return new spell_yogg_saron_malady_of_the_mind_AuraScript();
    }
};
"""

def replace_new_with_RegisterSpellScript(lines, script_name):
    script_name_search = "new "+script_name.replace('_aura','').replace('_spell','')
    for i, line in enumerate(lines):
        if script_name_search in line:
            new_line = f"    RegisterSpellScript({script_name});"
            lines[i] = new_line
            return lines

def format_first_block_in_file(path_in, path_out) -> None:
    with open(path_in, 'r') as file:
        lines = file.read();
        lines = lines.split('\n')
    out, spell_string, start_index, last_index, script_name = convert_function_block(lines)
    lines = lines[:start_index] + out.split('\n') + lines[last_index+2:] # TODO: Investigate why +2
    lines = replace_new_with_RegisterSpellScript(lines, script_name)
    if not path_out:
        path_out = path_in
    with open(path_out, 'w') as file:
        file.write('\n'.join(lines))
