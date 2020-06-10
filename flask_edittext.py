import sqlite3
from flask import g,Flask,request,render_template,redirect,url_for, session,escape
import random
import re
import os
from markupsafe import escape
app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

DATABASE = 'database/database_train.db'
app.secret_key = 'set contributer'
 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        session['contributer'] = request.form['contributer']
        session['load'] = 0
        print(session)
        return redirect('http://localhost:6006/random')
    return render_template('index.html')



@app.route('/thanks')
def tks():
    return render_template('thanks.html')

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


@app.route('/random',methods=['GET','POST'])
def random_id():
    if request.method == 'GET':
        cursor = get_db().cursor()

        sqlite_select_query = """SELECT * from dataset"""
        sqlite_select_query_edit = """SELECT dataset_id from dataset_correction"""

        cursor.execute(sqlite_select_query_edit)
        ids_edit = cursor.fetchall()

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        i = random.randint(0,len(records)-1)
        check = []

        for j in range(len(ids_edit)):
            check.append(ids_edit[j][0])
        while records[i][0] in check:
            i = random.randint(0,len(records)-1)

        session['id'] = records[i][0]
        cursor.close()
        _url = 'http://localhost:6006/random/' + str(session['id'])
        print(session)
        return redirect(_url)
        
@app.route('/random/<ids>',methods=['GET','POST'])
def randd(ids):
    load = session['load']
    id_edit = session['id']
    contributer_name = session['contributer']
    if request.method == 'GET':
        if load == 1:
            session['load'] = 0
            return redirect('http://localhost:6006/random')
        else:
            cursor = get_db().cursor()
            sqlite_select_query = """SELECT * from dataset"""
            sqlite_select_query_eng = """SELECT * from dataset_eng """

            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            cursor.execute(sqlite_select_query_eng)
            records_eng = cursor.fetchall()
            i = id_edit
            print(records_eng[i][1])
            question_eng = records_eng[i][1]
            context_eng = records_eng[i][2]
            answer_eng = records_eng[i][3]

            if str(records[i][3]) == 'None':
                answer = ''
                answer_eng =''
            else:
                answer = str(records[i][3])
                

            context = str(records[i][2])
            context_new = str(records[i][2])
            question = records[i][1]
            if answer!= '' and re.search(answer,context) != None:
                answer_rand = answer
            else:
                answer_rand = records[i][2][30:40]

            if str(answer_eng) !='' :
                answer_new = '<strong>'+answer_eng+'</strong>'
                context_eng_new = context_eng.replace(answer_eng,answer_new)
            else:
                context_eng_new = context_eng

            answer_start = records[i][4]
            session['answer_start'] = answer_start
            c_id = int(records[i][5])
            session['c_id'] = c_id
            impossible= records[i][6]
            cursor.close()
            

        ####Edit datatrain####

            answer_edit = None
            context_edit = None
            session['load'] = 1

    if request.method == 'POST':
        question_edit = request.form['question_edit']
        answer_edit = request.form['answer_edit']
        context_edit =request.form['context_edit']
        
        db= get_db()
        cursor = db.cursor()
        sqlite_insert_with_param = """INSERT INTO dataset_correction
                          (dataset_id ,question, context, answer, answer_start, c_id, contributer) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)"""

        if request.form.get('check_answer'):
            answer_edit =''
        
        data_tuple = (id_edit,question_edit,context_edit,answer_edit,session['answer_start'],session['c_id'],contributer_name)
        try: 
            cursor.execute(sqlite_insert_with_param, data_tuple)
        except sqlite3.IntegrityError:
            db.commit()
            cursor.close()
            session['load'] = 0
            return ('', 204)
        db.commit()
        cursor.close()
        session['load'] = 0
        return ('', 204)
    return render_template('edit_text.html',id_edit = id_edit, edits = answer_rand ,question = question,context = context ,context_new=context_new, answer = answer,question_eng = question_eng,context_eng=context_eng_new,answer_eng=answer_eng, contributer = contributer_name)
    

if __name__ == "__main__":
    app.run(port=6006)
