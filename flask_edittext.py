import sqlite3
from flask import g,Flask,request,render_template,redirect,url_for
import random
import re
import os
app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")
id_edit = 0
c_id = 0
impossible =''
answer_start = 0
question =''
DATABASE = 'database/database_train.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def find_text(answer_,context_,language_):
    tam = [0,len(context_)]
    context_new = ''
    answer_new = answer_[0].lower() + answer_[1:len(answer_)]
    if re.search(answer_new,context_) != None:
        answer_ = answer_new
    else:
        answer_new = answer_[0].upper() + answer_[1:len(answer_)]
        if re.search(answer_new,context_) != None:
            answer_ = answer_new
    for find in range(len(re.findall(answer_,context_))):
        if(find == 0):
            match = re.search(answer_,context_[tam[0]:len(context_)])
            new1 = match.start()
            new2 = match.end()
            context_new += context_[0:match.start()]
            if language_ == 'en':
                context_new += '<strong>' + context_[match.start():match.end()] + '</strong>'
            else:
                context_new += context_[match.start():match.end()]
            tam.pop(0)
            tam.pop(0)
            tam.append(match.start())
            tam.append(match.end())
        else:
            match = re.search(answer_,context_[tam[1]:len(context_)])
            new1 = tam[1]+match.start()
            new2 = match.end() + tam[1]
            tam.append(new1)
            tam.append(new2)
            context_new += context_[tam[1]:new1]
            if language_ == 'en':
                context_new += '<strong>' + context_[match.start():match.end()] + '</strong>'
            else:
                context_new += context_[match.start():match.end()]
            tam.pop(0)
            tam.pop(0)
    context_new += context_[new2:len(context_)]
    return context_new
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/thanks')
def tks():
    return render_template('thanks.html')
@app.route('/random',methods=['GET','POST'])
def randd():
    global id_edit
    global c_id
    global impossible
    global answer_start
    global question
    if request.method == 'GET':
        cursor = get_db().cursor()

        sqlite_select_query = """SELECT * from dataset"""
        sqlite_select_query_edit = """SELECT dataset_id from dataset_correction"""
        sqlite_select_query_eng = """SELECT * from dataset_eng """

        cursor.execute(sqlite_select_query_edit)
        ids_edit = cursor.fetchall()

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        cursor.execute(sqlite_select_query_eng)
        records_eng = cursor.fetchall()

        i = random.randint(0,len(records)-1)
        check = []

        for j in range(len(ids_edit)):
            check.append(ids_edit[j][0])
        while records[i][0] in check:
            i = random.randint(0,len(records)-1)
        id_edit =  records[i][0]
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
            context_new = find_text(answer,context,'vi')
        else:
            answer_rand = records[i][2][30:40]

        if str(answer_eng) !='' and re.search(answer_eng,context_eng) != None:
            context_eng_new = find_text(answer_eng,context_eng,'en')
        else:
            context_eng_new = context_eng
        id_edit = int(records[i][0])
        answer_start = records[i][4]
        c_id = int(records[i][5])
        impossible= records[i][6]
        cursor.close()
        

    ####Edit datatrain####

        
        answer_edit = None
        context_edit = None

    if request.method == 'POST':
        question_edit = request.form['question_edit']
        answer_edit = request.form['answer_edit']
        context_edit =request.form['context_edit']
        db= get_db()
        cursor = db.cursor()
        sqlite_insert_with_param = """INSERT INTO dataset_correction
                          (dataset_id ,question, context, answer, answer_start, c_id) 
                          VALUES (?, ?, ?, ?, ?, ?)"""

        if request.form.get('check_answer'):
            answer_edit =''
        
        data_tuple = (id_edit,question_edit,context_edit,answer_edit,answer_start,c_id)
        
        cursor.execute(sqlite_insert_with_param, data_tuple)
        db.commit()
        cursor.close()
        return redirect(url_for('tks'))
    return render_template('edit_text.html',id_edit = id_edit, edits = answer_rand ,question = question,context = context ,context_new=context_new, answer = answer,question_eng = question_eng,context_eng=context_eng_new,answer_eng=answer_eng)
    

if __name__ == "__main__":
    app.run(port=6006)
