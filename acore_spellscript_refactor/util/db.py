# connect with database
import re

import mysql.connector

from .colors import Color, color
from .logger import logger

HOST="localhost"
USER="acore"
PASSWORD="acore"
DATABASE="acore_world"

def format_spell_ids(spell_ids):
    logger.debug(f'{spell_ids=}')
    spell_ids_format = ','.join(str(spell_id) for spell_id in spell_ids)
    logger.debug(f'{spell_ids_format=}')
    spell_ids_format = '('+spell_ids_format+')'
    logger.debug(f'{spell_ids_format=}')
    return spell_ids_format

def generate_sql_update_script_name(script_name_original: str, script_name: str) -> str:
    try:
        spell_ids = db_lookup_ids(script_name_original)
    except mysql.connector.Error as error:
        logger.error(color(f"{error=}", Color.RED))
        logger.error(color(f"failed for {script_name=}. Incorrect database credentials", Color.RED))
        sql_update_script_name = """UPDATE `spell_script_names` SET `ScriptName`='{}' WHERE `spell_id`=XXXXX AND `ScriptName`='{}';\n""".format(script_name, script_name_original)
        return sql_update_script_name

    if len(spell_ids) == 0:
        logger.error(color(f'no spell_ids found for {script_name=}', Color.RED))
        return ''
    elif len(spell_ids) == 1:
        spell_id = spell_ids[0]
        sql_update_script_name = """UPDATE `spell_script_names` SET `ScriptName`='{}' WHERE `spell_id`={} AND `ScriptName`='{}';\n""".format(script_name, spell_id, script_name_original)
        return sql_update_script_name
    else:
        spell_ids_format = format_spell_ids(spell_ids)
        sql_update_script_name = """UPDATE `spell_script_names` SET `ScriptName`='{}' WHERE `spell_id` IN {} AND `ScriptName`='{}';\n""".format(script_name, spell_ids_format, script_name_original)
        return sql_update_script_name

def db_lookup_ids(script_name: str) -> list[int] :
    my_db = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    my_cursor = my_db.cursor()
    my_cursor.execute(f"SELECT `spell_id` FROM `spell_script_names` WHERE `ScriptName` = '{script_name}'")
    result = my_cursor.fetchall()
    ids = [x[0] for x in result]
    return ids