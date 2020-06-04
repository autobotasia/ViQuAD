import sqlite3
import pandas as pd

def updateSqliteTable(id, c_id):
    try:
        sqliteConnection = sqlite3.connect('database/database_train.db')
        cursor = sqliteConnection.cursor()
        
        sql_update_query_eng = """Update dataset_eng set answer = ? where id = ?"""
        sql_update_query_vi =   """Update dataset set c_id = ? where id = ?"""
        data_cid = (c_id,id)
        #cursor.execute(sql_update_query_eng, data_imp)
       #sqliteConnection.commit()
        cursor.execute(sql_update_query_eng, data_cid)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
        while True:
            sqliteConnection.close()
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("The sqlite connection is closed")
sqliteConnection = sqlite3.connect('database/database_train_fix.db')
cursor = sqliteConnection.cursor()            
sql_select_query_vi = """SELECT impossible from dataset""" 
sql_select_query_eng = """SELECT answer from dataset_eng""" 
cursor.execute(sql_select_query_vi)
records_imp = cursor.fetchall()
cursor.execute(sql_select_query_eng)
records_ans = cursor.fetchall()
for i in range(1,130320):
    if records_ans[i-1][0] == 'nan':
        answer_ = None
        updateSqliteTable(i,answer_)
        print('Completed ',i)


































































































































































































































