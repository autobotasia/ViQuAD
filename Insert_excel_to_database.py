import sqlite3
import pandas as pd
data = pd.read_excel('./data_translate/data_train.xlsx')
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

    except sqlite3.Error  as error:
        print("Failed to insert Python variable into sqlite table", error)
        #print('Error at: ', i)
        a = 0
        while(True):
            sqliteConnection.close()
            if a == 0:
                print('Ctrl+C to exit')
                a += 1

    
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            # if i%5000 == 0:
            #     print('Completed',i,'row')


#insert file english or trans:
for i in range(1,len(data['id'])+1):
    try:
    #     if data['impossible'][i-1] == 0:
    #         data_imp = 'False'
    #     else:
    #         data_imp = 'True'
        if str(data['answer'][i-1]) == 'nan' and data['impossible'][i-1] == 'TRUE':
            data_ans = ''
        else:
            data_ans = str(data['answer'][i-1])
        insertVaribleIntoTable(i,data['question'][i-1],data['context'][i-1],data_ans,data['answer_start'][i-1],int(data['c_id'][i-1]),data['impossible'][i-1])
    
    except ValueError as error:
        print('ValueError:',error ,'and Error at:', i)
        a = 0
        while(True):
            if a == 0:
                print('Ctrl+C to exit')
                a += 1
                
    except TypeError as error:
        print('TypeError:',error ,'and Error at:', i)
        a = 0
        while(True):
            if a == 0:
                print('Ctrl+C to exit')
                a += 1
    
