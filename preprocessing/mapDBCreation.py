import sqlite3
from readGraph import readPickled

db = sqlite3.connect("IDTitleDB.sqlite")
c = db.cursor()

c.execute("create table if not exists IDTitle (ID integer, title text)")

input_file = "C:/02807Project_Data/idtotitlemapNoRedirect"

map = readPickled(input_file)

for ID in map:
    t = (ID, map[ID])
    c.execute("insert into IDTitle (ID, title) values (?,?)", t)
db.commit()
