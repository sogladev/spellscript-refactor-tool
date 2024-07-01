import os
import pytest

import mysql.connector

from acore_spellscript_refactor.util.db import *

ENV_GITHUB_CI = "CI"

def test_always_passes():
    assert True

@pytest.mark.skipif(os.getenv(ENV_GITHUB_CI) is not None, reason="skip this test in CI")
def test_db_lookup_ids_empty():
    result = db_lookup_ids('this_spell_does_not_exist_12379832')
    assert len(result) == 0


@pytest.mark.skipif(os.getenv(ENV_GITHUB_CI) is not None, reason="skip this test in CI")
def test_db_lookup_ids_single_spell():
    result = db_lookup_ids('spell_gen_proc_not_self')
    assert result[0] == 70803
    assert len(result) == 1

def test_format_spell_ids():
    spell_ids_format = format_spell_ids([1, 2, 3, 4])
    format_expected = '(1,2,3,4)'
    assert spell_ids_format == format_expected

@pytest.mark.skipif(os.getenv(ENV_GITHUB_CI) is not None, reason="skip this test in CI")
def test_db_write_sql():
    script_name = 'spell_gen_proc_not_self'
    result = db_lookup_ids(script_name)
    assert result[0] == 70803
    sql = generate_sql_update_script_name(script_name, script_name)
    sql_expected ="""UPDATE `spell_script_names` SET `ScriptName`='spell_gen_proc_not_self' WHERE `spell_id`=70803 AND `ScriptName`='spell_gen_proc_not_self';\n"""
    assert sql == sql_expected

@pytest.mark.skipif(os.getenv(ENV_GITHUB_CI) is not None, reason="skip this test in CI")
def test_db_write_sql_with_original():
    script_name_original = 'spell_gen_proc_not_self'
    script_name = 'spell_gen_proc_not_self_aura'
    result = db_lookup_ids(script_name_original)
    assert result[0] == 70803
    sql = generate_sql_update_script_name(script_name_original, script_name)
    sql_expected ="""UPDATE `spell_script_names` SET `ScriptName`='spell_gen_proc_not_self_aura' WHERE `spell_id`=70803 AND `ScriptName`='spell_gen_proc_not_self';\n"""
    assert sql == sql_expected

@pytest.mark.skipif(os.getenv(ENV_GITHUB_CI) is not None, reason="skip this test in CI")
def test_db_write_sql_fail():
    script_name = 'doesnotexist123823'
    result = db_lookup_ids(script_name)
    assert len(result) == 0
    sql = generate_sql_update_script_name(script_name, script_name)
    sql_expected = ''
    assert sql == sql_expected

def test_failed_connection():
    try:
        mysql.connector.connect(
            host="localhost",
            user="acore",
            password="wrongpassword",
            database="acore_world"
        )
    except mysql.connector.Error:
        assert True
        return
    assert False