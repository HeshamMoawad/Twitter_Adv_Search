import pandas
import sqlite3

con = sqlite3.connect("Data\Database.db")
cur = con.cursor()

df = pandas.read_excel("Data\جروبات..xlsx")
print()
for link in df["اللينك"]:
    cur.execute(f"""INSERT INTO links ('Link')VALUES("{link}");""")
    con.commit()
con.close()




