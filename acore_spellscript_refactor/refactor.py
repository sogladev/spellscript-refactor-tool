import re
from enum import Enum
from typing import Union
from pathlib import Path

from .util.colors import Color, color
from .util.logger import logger
from .util.db import generate_sql_update_script_name

class ScriptType(Enum):
    AURA = 1
    SPELL = 2
    PAIR = 3

def find_start_last_index(lines_to_search):
    start_index = None
    for i, line in enumerate(lines_to_search):
        if (start_index is None and re.match("class .* : public SpellScriptLoader", line)):
            start_index = i
        if (start_index is None and re.match("class .* : SpellScriptLoader", line)):
            start_index = i
        if start_index:
            logger.debug(f"{i:,=} {line=}")
            if line.rstrip() == '};':
                return start_index, i
    logger.error(color(f"No spells scripts found", Color.RED))
    raise ValueError

def find_name_of_script(lines_to_search, start_index=0):
    count = 0
    class_name_found = False
    loader_name = None
    for line in lines_to_search[start_index:]:
        logger.debug(f"{line=}")
        if ': SpellScriptLoader(' not in line and 'class ' in line and ("public SpellScriptLoader" in line or ": SpellScriptLoader" in line):
            class_name = re.findall(r'class ([\w_]+)', line)[0]
            logger.debug(f"{class_name=}")
            class_name_found = True
        if ': SpellScriptLoader(' in line:
            loader_name_found = re.findall(r'SpellScriptLoader\("([\w_]+)"\)', line)
            if len(loader_name_found) > 0:
                logger.debug(f"{line=} loader_name not found: skipping")
                loader_name = loader_name_found[0][:]
                logger.debug(f"{loader_name=}")
        if class_name_found:
            count +=1
        if count >= 4:
            return loader_name if loader_name is not None else class_name

def get_script_type(lines_to_search, start_index=0) -> ScriptType:
    isAuraScript = None
    isSpellScript = None
    for line in lines_to_search[start_index:]:
        logger.debug(f"line=")
        if "AuraScript" in line:
            logger.debug(f"AuraScript {line=}")
            isAuraScript = True
        if "SpellScript" in line and not "SpellScriptLoader" in line:
            logger.debug(f"SpellScript {line=}")
            isSpellScript = True
        if line.rstrip() == "};":
            break
    if isAuraScript and isSpellScript:
        return ScriptType.PAIR
    elif isAuraScript:
        return ScriptType.AURA
    elif isSpellScript:
        return ScriptType.SPELL
    else:
        logger.error(color("Unable to determine type!", Color.RED))

def find_register_start_end_index(lines_to_search, start_index=0):
    start = None
    logger.debug(f"{start_index=}")
    for i, line in enumerate(lines_to_search[start_index:]):
        logger.debug(f"{i:03};{line}")
        if 'void Register' in line:
           start = i
        if start:
            if line.strip() == '}':
                absolute_start = start+start_index
                absolute_end = i+start_index
                logger.debug(f"{start:,=};{absolute_start:,=} {lines_to_search[start]}")
                logger.debug(f"{i:,=};{absolute_end:,=} {lines_to_search[i]}")
                return absolute_start, absolute_end

def find_register_statements(lines, start_index):
    register_index_start, register_index_bracket = find_register_start_end_index(lines[start_index:])
    register_index_start += start_index
    register_index_bracket += start_index
    register_statements = lines[register_index_start+2:register_index_bracket]
    logger.debug(f"{register_index_start:,=};{register_index_bracket:,=}")
    for i, dbg_out in enumerate(register_statements):
        logger.debug(f"{i:03}:{dbg_out}")
    return register_statements

def format_register_statements(register_statements, original=None, new=None):
    register_statements_format = []
    for c in register_statements:
        if c.strip() == '':
            c = ''
        else:
            c = 8*' ' + c.lstrip()
            c = c.replace('_AuraScript','_aura').replace('_aura_aura','_aura')
            c = c.replace('AuraScript','_aura').replace('_aura_aura','_aura')
            c = c.replace('_SpellScript','')
            c = c.replace('SpellScript','')
            if original is not None and new is not None:
                c = c.replace(original+'Script',new)
        register_statements_format.append(c)
    for i, dbg_out in enumerate(register_statements):
        logger.debug(f"before:{i:03}:{dbg_out}")
    for i, dbg_out in enumerate(register_statements_format):
        logger.debug(f"after :{i:03}:{dbg_out}")
    return register_statements_format

def find_content_start_end_index(lines_to_search, start_index=0, script_name=''):
    start = None
    for i, line in enumerate(lines_to_search[start_index:]):
        if any(p in line for p in ['PrepareAuraScript', 'PrepareSpellScript']):
            start = i
        if start:
            if 'void Register' in line:
                absolute_start = start+start_index
                absolute_end = i+start_index
                logger.debug(f"{absolute_start=},{absolute_end=}")
                return start+start_index, i+start_index

def find_spells_to_validate(line) -> list[str]:
    cases_to_validate = [
        '->CastCustomSpell(',
        '->CastSpell(',
        '->ApplySpellImmune',
        '->HasAura(',
        '->GetAuraCount(',
        '->RemoveAurasDueToSpell('
    ]
    if any(c in line for c in cases_to_validate ):
        logger.debug(f"{line=}")
        spells = []
        spells_found = re.findall('(SPELL_[A-Z_0-9]{,}|[0-9]{4,})', line)
        for spell in spells_found:
            logger.debug(f"{spell=}")
            if spell not in spells:
                spells.append(spell)
        return spells
    return []

def format_spells(spells):
    return ', '.join(spells)

def format_validate_function(spells) -> str:
    spells_formatted = format_spells(spells)
    out ="""
    bool Validate(SpellInfo const* /*spellInfo*/) override
    {
        return ValidateSpellInfo({ """+spells_formatted+""" });
    }\n"""
    return out

def create_validate_lines(lines_to_search, start_index=0) -> str:
    logger.debug(f"{start_index=}")
    spells = []
    for i, line in enumerate(lines_to_search[start_index:]):
        logger.debug(f"{i:03};{line}")
        spells_found = find_spells_to_validate(line)
        for spell in spells_found:
            if spell not in spells:
                spells.append(spell)
        if 'void Register' in line:
            break
    if len(spells) == 0:
        return ''
    formatted = format_validate_function(spells)
    logger.debug(f"{formatted=}")
    return formatted

def find_variables(lines, start_index=0) -> tuple[bool, int, int]:
    start = None
    end = None
    foundRegister = False
    foundEndRegister = False
    foundVariables = False
    for i, line in enumerate(lines[start_index:]):
        logger.debug(line)
        if line.rstrip() == '};':
            start = 0
            end = i
            break
        if 'void Register' in line:
            logger.debug("Found register")
            foundRegister = True
        if foundRegister and (line == 8*" "+"}" or line == 8*" "+"};"):
            start = i + 1
            foundEndRegister = True
            logger.debug("Found end register")
            logger.debug(f"{i+start_index} {line}")
        if foundEndRegister and ("protected:" in line or "public:" in line or "private:" in line):
            logger.debug("Found variable")
            logger.debug(f"{i+start_index}")
            logger.debug(line)
            foundVariables = True
        if foundRegister and (line == '    };' or line == '};'):
            end = i
            break
    # if start is None or end is None:
     #    return foundVariables, start_index, start_index
    # else:
    return foundVariables, start+start_index, end+start_index

def find_content_statements(lines, start_index):
    content_index_start, content_index_end = find_content_start_end_index(lines[start_index:])
    content_index_start += start_index
    content_index_end += start_index
    content_statements = lines[content_index_start+1:content_index_end]
    return content_statements

def format_content_statements(content_statements, original=None, new=None):
    content_statements_format = []
    for c in content_statements:
        if c.strip() == '':
            c = ''
        elif 8*' ' in c:
            c = (4*' ').join(c.split(4*' ')[1:])
        c = c.replace('_AuraScript','_aura').replace('_aura_aura','_aura')
        c = c.replace('_SpellScript','')
        if original is not None and new is not None:
            c = c.replace(original+'Script',new)
        content_statements_format.append(c)
    for i, dbg_out in enumerate(content_statements):
        logger.debug(f"before:{i:03}:{dbg_out}")
    for i, dbg_out in enumerate(content_statements_format):
        logger.debug(f"after :{i:03}:{dbg_out}")
    return content_statements_format

def format_variables(variables):
    formatted_variables = []
    for c in variables:
        if c.strip() == '':
            continue
        elif 4*' ' in c:
            c = (4*' ').join(c.split(4*' ')[1:])
        formatted_variables.append(c)
    return formatted_variables

def is_validate_in_content(content_statements):
    return any('bool Validate(' in c for c in content_statements)

def find_constructor_statement(lines_to_search, start_index) -> str:
    has_public = False
    for i, line in enumerate(lines_to_search[start_index:]):
        if any(p in line for p in ['PrepareAuraScript', 'PrepareSpellScript']):
            return ''
        if 'public:' in line.lstrip():
            has_public = True
        if has_public and ': SpellScriptLoader(name' in line:
            return line
    return ''

def format_content_statement(line):
    # input = 'spell_hadronox_summon_periodic(const char* name, uint32 delay, uint32 spellEntry) : SpellScriptLoader(name), _delay(delay), _spellEntry(spellEntry) { }'
    # expected = 'spell_hadronox_summon_periodic_aura(uint32 delay, uint32 spellEntry) : _delay(delay), _spellEntry(spellEntry) { }'
    line = line.replace('const char* name, ','')
    line = line.replace('SpellScriptLoader(name), ','')
    return line

def convert_aura_or_spell_script(lines, start_index, last_index, script_type, script_name, original_script_name) -> tuple[list[str], ScriptType, int, int, str, str]:
    type = 'SpellScript' if script_type == ScriptType.SPELL else 'AuraScript'
    prepare = 'Spell' if script_type == ScriptType.SPELL else 'Aura'
    register_statements = find_register_statements(lines, start_index)
    register_statements = format_register_statements(register_statements, original=original_script_name, new=script_name)
    content_statements = find_content_statements(lines, start_index)
    constructor_statement = find_constructor_statement(lines, start_index)
    constructor_statement = constructor_statement.replace(original_script_name, script_name)
    constructor_statement_formatted = format_content_statement(constructor_statement)
    constructor = f"\npublic:\n{constructor_statement_formatted}\n" if constructor_statement else ''
    validate = create_validate_lines(lines, start_index) if not is_validate_in_content(content_statements) else ''
    content_statements = format_content_statements(content_statements, original=original_script_name, new=script_name)

    content: str = '\n'.join(content_statements)
    register_formatted: str = '\n'.join(register_statements)
    isVariables, start, end = find_variables(lines, start_index)
    if not isVariables:
        variables = ''
    else:
        variables = 2*'\n'+'\n'.join(format_variables(lines[start:end]))
    out_formatted = \
"""class """+script_name+""" : public """+type+"""\n{
    Prepare"""+prepare+"""Script("""+script_name+");\n"+constructor+validate\
+content+\
"""
    void Register() override
    {\n"""+\
register_formatted+\
"""
    }"""+variables+"""
};"""
    for i, dbg_out in enumerate(lines[start_index:last_index+1]):
        logger.debug(f"before:{i:03}:{dbg_out}")
    for i, dbg_out in enumerate(out_formatted.split('\n')):
        logger.debug(f"after :{i:03}:{dbg_out}")

    return out_formatted, script_type, start_index, last_index, script_name, original_script_name

def find_spell_block_in_pair(lines, script_type):
    reg = None
    if script_type == ScriptType.AURA:
        reg = ".*class .*_AuraScript : public AuraScript.*"
    elif script_type == ScriptType.SPELL:
        reg = ".*class .*_SpellScript : public SpellScript.*"
    else:
        logger.error(color("Invalid type", Color.RED))

    start_index = None
    end_index = None
    for i, line in enumerate(lines):
        if (start_index is None and re.match(reg, line)):
            start_index = i
        if start_index:
            logger.debug(f"{i:,=} {line=}")
            if line.rstrip() == '    };':
                end_index = i
                break
    return lines[start_index:end_index+1]

def format_script_name(script_name, script_type):
    if script_type == ScriptType.AURA:
        return (script_name + '_aura').replace('_aura_aura','_aura')
    elif script_type == ScriptType.SPELL:
        return script_name
    elif script_type == ScriptType.PAIR:
        return script_name

def convert_function_block(lines: list[str]) -> tuple[str, ScriptType, int, int, str, str]:
    start_index, last_index = find_start_last_index(lines)
    logger.debug(f"{start_index=}{last_index=}")
    script_type = get_script_type(lines, start_index)
    logger.debug(f"{script_type=}")
    script_name = find_name_of_script(lines, start_index)
    original_script_name = script_name
    formatted_script_name = format_script_name(script_name, script_type)
    logger.debug(f"{script_name=}")
    if script_type != ScriptType.PAIR:
        return convert_aura_or_spell_script(lines, start_index, last_index, script_type, formatted_script_name, original_script_name)
    spell_script_lines = find_spell_block_in_pair(lines[start_index:last_index], ScriptType.SPELL)
    formatted_script_name = format_script_name(script_name, ScriptType.SPELL)
    converted_spell, _, _, _, _, _ = convert_aura_or_spell_script(spell_script_lines, 0, len(spell_script_lines), ScriptType.SPELL, formatted_script_name, original_script_name)

    aura_script_lines = find_spell_block_in_pair(lines[start_index:last_index], ScriptType.AURA)
    formatted_script_name = format_script_name(script_name, ScriptType.AURA)
    converted_aura, _, _, _, _, _ = convert_aura_or_spell_script(aura_script_lines, 0, len(aura_script_lines), ScriptType.AURA, formatted_script_name, original_script_name)

    return (converted_spell, converted_aura), script_type, start_index, last_index, script_name, original_script_name

ARGS_REGISTER_LINES = []

def format_RegisterSpellScript(script_name, script_type: ScriptType, args=None) -> str:
    if script_type == ScriptType.PAIR:
        register_statement = f"    RegisterSpellAndAuraScriptPair({script_name}, {script_name}_aura);"
    elif args is not None:
        if script_type == ScriptType.AURA:
            ARGS_REGISTER_LINES.append(args[0].replace('"',''))
            args[0] = args[0][:-1]+'_aura"'
        register_statement = f"    RegisterSpellScriptWithArgs({script_name}, {', '.join(args)});"
    else:
        register_statement = f"    RegisterSpellScript({script_name});"
    logger.debug(f"{register_statement=}")
    return register_statement

def remove_aura_spell_suffix(script_name):
    script_name_without_aura_suffix = re.sub('_aura$', '', script_name)
    script_name_without_aura_spell_suffix = re.sub('_spell$', '', script_name_without_aura_suffix)
    return script_name_without_aura_spell_suffix


def replace_new_with_RegisterSpellScript(lines, script_name, script_type):
    script_name_search = "new "+ remove_aura_spell_suffix(script_name)
    logger.debug(f"{script_name=}")
    logger.debug(f"{script_type=}")
    logger.debug(f"{script_name_search=}")
    logger.debug(f"{lines}")
    foundVoidSc = False
    hasArguments = False
    for i, line in enumerate(lines):
        if line.startswith("void AddSC_"):
            foundVoidSc = True
        if foundVoidSc and script_name_search in line:
            logger.debug(f"{script_name_search=}")
            logger.debug(f"{script_name=}")
            if line.endswith("();"):
                new_line = format_RegisterSpellScript(script_name, script_type)
                logger.debug(f"before:{lines[i]}")
                lines[i] = new_line
                logger.debug(f"after :{new_line}")
                return lines, None
            else:
                args_found = re.findall('new \w+\((.+)\);', line)
                args = [s.strip() for s in args_found[0].split(',')]
                new_line = format_RegisterSpellScript(script_name, script_type, args=args)
                lines[i] = new_line
                logger.debug(f"after :{new_line}")
                hasArguments = True
    if hasArguments:
        return lines, args[0] # return name
    logger.error("No register name found")


def format_first_block_in_file(path_in, path_out, skip=0, sql_path='script_name_updates.sql', create_commit=False):
    logger.info(f"{path_in=}")
    logger.info(f"{path_out=}")
    logger.info(f"{sql_path=}")
    with open(path_in, 'r') as file:
        lines = file.read();
        lines = lines.split('\n')
    logger.debug(f"{len(lines)=} {path_in=}")
    out, script_type, start_index, last_index, script_name, original_script_name = convert_function_block(lines[skip:])
    if type(out) == tuple:
        spell, aura = out
        out = spell + 2*'\n' + aura
    lines = lines[:start_index+skip] + out.split('\n') + lines[last_index+skip+1:]
    lines, arg_name = replace_new_with_RegisterSpellScript(lines, script_name, script_type)

    for i, dbg_out in enumerate(lines):
        logger.debug(f"{i:03}:{dbg_out}")
    with open(path_out, 'w') as file:
        file.write('\n'.join(lines))
        logger.info(color(f"{script_name=}", Color.GREEN))

    hasUpdateQuery = False
    if script_type != ScriptType.AURA or original_script_name == script_name:
        logger.info(color(f"Skipped query for {original_script_name=}", Color.YELLOW))
    elif script_type == ScriptType.AURA:
        with open(sql_path, 'a') as file:
            sql_update_script_name = generate_sql_update_script_name(original_script_name, script_name)
            if sql_update_script_name == '':
                logger.error(color(f"Update is empty for {original_script_name=}:{script_name=}", Color.RED))
            else:
                logger.debug(f"{sql_update_script_name=}")
                file.write(sql_update_script_name)
                hasUpdateQuery = True
                logger.info(color(f"Appended {script_name} to {Path(sql_path).name}", Color.GREEN))
        if arg_name is not None:
            with open(sql_path, 'a') as file:
                for arg_name in ARGS_REGISTER_LINES:
                    arg_name_new = arg_name+'_aura' if not arg_name.endswith('_aura') else arg_name
                    if arg_name != arg_name_new:
                        sql_update_script_name = generate_sql_update_script_name(arg_name, arg_name_new)
                        if sql_update_script_name == '':
                            logger.error(color(f"Update query is empty for {original_script_name=}:{script_name=}", Color.RED))
                        else:
                            logger.debug(f"{sql_update_script_name=}")
                            file.write(sql_update_script_name)
                            hasUpdateQuery = True
                            logger.info(color(f"Appended {arg_name_new} to {Path(sql_path).name}", Color.GREEN))

    if create_commit:
        from os import system
        script_type_name = "pair"
        if script_type == ScriptType.AURA:
            script_type_name = "aura"
        elif script_type == ScriptType.SPELL:
            script_type_name = "spell"
        system("git reset") # unstage all
        if sql_path != "script_name_updates.sql" and hasUpdateQuery:
            system(f"git add {sql_path}")
        if path_in == path_out:
            system(f"git add {path_out}")
        filename_stem = Path(path_out).stem
        message = f"\"{filename_stem} {script_type_name}:{script_name}\""
        system(f"git commit -m {message}")

