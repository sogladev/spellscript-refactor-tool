import pytest

import mysql.connector

from acore_spellscript_refactor.util.db import *

def test_always_passes():
    assert True

def test_db_lookup_ids_empty():
    result = db_lookup_ids('this_spell_does_not_exist_12379832')
    assert len(result) == 0

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