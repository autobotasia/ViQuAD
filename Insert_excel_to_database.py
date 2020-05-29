import sqlite3
import pandas as pd
data = pd.read_excel('./data_translate/dataset_train.xlsx')
def insertVaribleIntoTable(id ,question, context, answer, answer_start, c_id, impossible):
    try:
        sqliteConnection = sqlite3.connect('database/database_train.db')
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO dataset
                          (id ,question, context, answer, answer_start, c_id, impossible) 
                          VALUES (?, ?, ?, ?, ?, ?, ?);"""
        #sqlite_update_poss = """Update SqliteDb_developers set impossible = ? where id = ?"""
        data_tuple = (id ,question, context, answer, answer_start, c_id, impossible)
        #data_imp = (impossible,id)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        #cursor.execute(sqlite_update_poss,data_imp)
        sqliteConnection.commit()
        #print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        print('Error in:', i)
        while(True):
            sqliteConnection.close()
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            if i%5000 == 0:
                print('Completed',i,'row')
for i in range(1,len(data['id'])+1):
    insertVaribleIntoTable(i,data['câu hỏi'][i-1],data['bối cảnh'][i-1],str(data['bản văn'][i-1]),data['answer_start'][i-1],data['c_id'][i-1],str(data['is_impossible'][i-1]))
   