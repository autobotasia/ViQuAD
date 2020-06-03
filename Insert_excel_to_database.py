import sqlite3
import pandas as pd
data = pd.read_excel('./data_translate/train_eng.xlsx')
def insertVaribleIntoTable(id ,question, context, answer, answer_start, c_id, impossible):
    try:
        sqliteConnection = sqlite3.connect('database/database_train.db')
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO dataset_eng
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
            print('Ctrl+C to exit')
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            if i%5000 == 0:
                print('Completed',i,'row')

#insert file translate:
#for i in range(1,len(data['id'])+1):
#    insertVaribleIntoTable(i,data['câu hỏi'][i-1],data['bối cảnh'][i-1],data['bản văn'][i-1],data['answer_start'][i-1],data['c_id'][i-1],str(data['is_impossible'][i-1]))

#insert file english:
for i in range(1,len(data['id'])+1):
    insertVaribleIntoTable(i,data['question'][i-1],data['context'][i-1],data['text'][i-1],data['answer_start'][i-1],data['c_id'][i-1],str(data['is_impossible'][i-1]))