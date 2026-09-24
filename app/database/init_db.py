import sqlite3

DATABASE_PATH = "data/database/nova_corp.db"

connection = sqlite3.connect(DATABASE_PATH)

print("NOVA Corp database created successfully!")

connection.close()