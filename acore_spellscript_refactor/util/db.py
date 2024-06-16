# connect with database
import mysql.connector

MYDB = mysql.connector.connect(
  host="localhost",
  user="acore",
  password="acore",
  database="acore_world"
)

def db_lookup_ids(script_name: str) -> list[int] :
    mycursor = MYDB.cursor()

    mycursor.execute(f"SELECT `spell_id` FROM `spell_script_names` WHERE `ScriptName` = '{script_name}'")

    myresult = mycursor.fetchall()

    ids = []
    for x in myresult:
        ids.append(x[0])

    return ids