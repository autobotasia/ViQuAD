import sqlite3
from flask import g,Flask,request,render_template,redirect,url_for
import random
app = Flask(__name__)
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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
    global question
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
        if str(records[i][3]) == 'nan':
            answer = ''
        else:
             answer = str(records[i][3])
        datatrain ='<br><strong>ID:</strong> '+str(records[i][0]) +" <br> <strong>Question: </strong> " + str(records[i][1]) +'</br><strong>Context:</strong> ' + str(records[i][2]) + '</br><strong>Answer:</strong> ' + answer
        id_edit = int(records[i][0])
        answer_start = records[i][4]
        c_id = int(records[i][5])
        impossible= records[i][6]
        cursor.close()
        
    ####Edit datatrain####

        question = records[i][1]
        answer_edit = None
        context_edit = None

    if request.method == 'POST':
        answer_edit = request.form['answer_edit']
        context_edit =request.form['context_edit']
        db= get_db()
        cursor = db.cursor()
        sqlite_insert_with_param = """INSERT INTO dataset_correction
                          (dataset_id ,question, context, answer, answer_start, c_id) 
                          VALUES (?, ?, ?, ?, ?, ?)"""
        data_tuple = (id_edit,question,context_edit,answer_edit,answer_start,c_id)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        db.commit()
        cursor.close()
        return redirect(url_for('tks'))
    return render_template('edit_text.html',datatrain = datatrain, context=records[i][2], answer = answer)
    

if __name__ == "__main__":
    app.run(port = 6006)
