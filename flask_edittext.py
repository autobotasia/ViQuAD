import sqlite3
from flask import g,Flask,request,render_template,redirect,url_for
import random
app = Flask(__name__)
a = 0 
id_edit = 0
c_id = 0
impossible =''
answer_start = 0
DATABASE = 'datasets_train.db'
database_edit = 'database_train_edit.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_db_edit():
    db_edit = sqlite3.connect(database_edit)
    return db_edit

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

    db_edit = getattr(g, '_database', None)
    if db_edit is not None:
        db_edit.close()

@app.route('/')
def index():
    return 'Hello'
@app.route('/thanks')
def tks():
    return render_template('thanks.html')
@app.route('/random',methods=['GET','POST'])
def randd():
    global id_edit
    global c_id
    global impossible
    global answer_start
    if request.method == 'GET':
        cursor = get_db().cursor()
        db_edit = get_db_edit()
        cursor_edit = db_edit.cursor()
        sqlite_select_query = """SELECT * from SqliteDb_developers"""
        sqlite_select_query_edit = """SELECT id from SqliteDb_developers"""
        cursor_edit.execute(sqlite_select_query_edit)
        cursor.execute(sqlite_select_query)
        ids_edit = cursor_edit.fetchall()
        records = cursor.fetchall()
        i = random.randint(0,len(records)-1)
        check = []
        for j in range(len(ids_edit)):
            check.append(ids_edit[j][0])
        while records[i][0] in check:
            i = random.randint(0,len(records)-1)
        datatrain ='<br><strong>ID:</strong> '+str(records[i][0]) +" <br> <strong>Question:</strong> " + str(records[i][1]) +'</br><strong>Context:</strong> ' + str(records[i][2]) + '</br><strong>Answer:</strong> ' + str(records[i][3])
        id_edit = int(records[i][0])
        answer_start = records[i][4]
        c_id = int(records[i][5])
        impossible= records[i][6]
        cursor.close()
        cursor_edit.close()
        if str(records[i][3]) == 'None':
            answer = ''
        else:
             answer = records[i][3]
    ####Edit datatrain####

        question_edit = None
        answer_edit = None
        context_edit = None

    if request.method == 'POST':
        db_edit = get_db_edit()
        cursor_edit = db_edit.cursor()
        question_edit = request.form['question_edit']
        answer_edit = request.form['answer_edit']
        context_edit =request.form['context_edit']
        #db_edit = get_db_edit()
        #cursor_edit = db_edit.cursor()
        sqlite_insert_with_param = """INSERT INTO SqliteDb_developers
                          (id ,question, context, answer, answer_start, c_id, impossible) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)"""
        data_tuple = (id_edit,question_edit,context_edit,answer_edit,answer_start,c_id,impossible)
        cursor_edit.execute(sqlite_insert_with_param, data_tuple)
        db_edit.commit()
        cursor_edit.close()
        return redirect(url_for('tks'))
    return render_template('edit_text.html',datatrain = datatrain, question = records[i][1], context=records[i][2], answer = answer)
    

if __name__ == "__main__":
    app.run()
