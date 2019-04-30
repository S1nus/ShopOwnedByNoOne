import sqlite3

conn = sqlite3.connect("tokens.db")
cur = conn.cursor()

sql = '''INSERT INTO tokens (address, token)
		VALUES(?, ?)''' 

try:
	cur.execute(sql, ('0x8ad7fa7dsf7adf', 'thiswasparameterized'))
except Error as e:
	print(e)

print(cur.lastrowid)
