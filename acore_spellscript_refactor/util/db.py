# connect with database
import mysql.connector

MYDB = mysql.connector.connect(
  host="localhost",
  user="acore",
  password="acore",
  database="acore_world"
)

def db_lookup_ids(spell_script_name: str) -> list[str] :
    return []
