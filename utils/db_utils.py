import sqlite3

def connect_db(path="database/agro_system.db"):
    return sqlite3.connect(path)
