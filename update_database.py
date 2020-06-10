import sqlite3
import pandas as pd

def updateSqliteTable(id, c_id):
    try:
        sqliteConnection = sqlite3.connect('database/database_train.db')
        cursor = sqliteConnection.cursor()
        
        sql_update_query_eng = """Update dataset_eng set id = ? where id = ?"""
        #sql_update_query_vi =   """Update dataset set id = ? where id = ?"""
        data_cid = (c_id,id)
        #cursor.execute(sql_update_query_vi, data_cid)
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

sqliteConnection = sqlite3.connect('database/database_train.db')
for i in range(66603,130321):
        updateSqliteTable(i+1,i)
        print('Completed ',i)


































































































































































































































