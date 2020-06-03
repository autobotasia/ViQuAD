import sqlite3

try:
    sqliteConnection = sqlite3.connect('./database/database_train.db')
    sqlite_create_table_query = '''CREATE TABLE dataset (
                                id INTEGER PRIMARY KEY,
                                question TEXT NOT NULL,
                                context TEXT NOT NULL,
                                answer TEXT,
                                answer_start INTEGER,
                                c_id INTEGER,
                                impossible TEXT)'''
    sqlite_create_table_query_correct = '''CREATE TABLE dataset_correction (
                                dataset_id INTEGER PRIMARY KEY,
                                question TEXT NOT NULL,
                                context TEXT NOT NULL,
                                answer TEXT,
                                answer_start INTEGER,
                                c_id INTEGER)'''
    sqlite_create_table_query_eng = '''CREATE TABLE dataset_eng (
                                id INTEGER PRIMARY KEY,
                                question TEXT NOT NULL,
                                context TEXT NOT NULL,
                                answer TEXT,
                                answer_start INTEGER,
                                c_id INTEGER,
                                impossible TEXT)'''
    cursor = sqliteConnection.cursor()
    
    print("Successfully Connected to SQLite")
    #cursor.execute(sqlite_create_table_query)
    #sqliteConnection.commit()
    #cursor.execute(sqlite_create_table_query_correct)
    #sqliteConnection.commit()
    cursor.execute(sqlite_create_table_query_eng)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")