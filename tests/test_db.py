import pytest

from acore_spellscript_refactor.util.db import *

def test_always_passes():
    assert True

def test_db_lookup_ids():
    result = db_lookup_ids('test')
    assert len(result) == 0