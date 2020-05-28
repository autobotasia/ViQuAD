import sqlite3

try:
    sqliteConnection = sqlite3.connect('./database/database_train_edit.db')
    sqlite_create_table_query = '''CREATE TABLE SqliteDb_developers (
                                id INTEGER PRIMARY KEY,
                                question TEXT NOT NULL,
                                context TEXT NOT NULL,
                                answer TEXT,
                                answer_start INTEGER,
                                c_id INTEGER,
                                impossible TEXT);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")