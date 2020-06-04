# ViQuAD

## Setup

This part of the library has only be tested with Python3.6+. 
There are few specific dependencies to install before launching a distillation, 
you can install them with the command `pip install -r requirements.txt`.

## How to use ViQuAD

Use data from SQuAD2.0

### Export Data

First, we will use file `extract_json_to_csv.py` export data in `./data` from file .json to csv. The files will be split, use Microsoft Excel change from `file.csv` to `file.xlsx` and translate document in:

`https://translate.google.com.vn/?hl=vi&tab=TT#view=home&op=docs&sl=en&tl=vi`

and save at `./data/translate` (use Microsoft Excel to merge small files together)

### Edit Data translate

Because use translate so data willbe wrong.

Creat database in the format: (id, question, context, answer, answer_start, c_di, impossible): `creat_database.py`

Insert data from excel (translated) to database: `Insert_excel_to_database.py`

Finally, Use `flask_edittext.py` to Edit data wrong

## Use Tool

Purpose: edit data (Here is: `Context` and `Quesion`) correct if translated wrong or not reasonable

After run `flask_edittext.py`

Interface:

<img width="964" alt="interface" src="https://raw.githubusercontent.com/autobotasia/ViQuAD/master/images/giaodien.png">

### Include:

- `Question`, `Context`, `Answer`: data has been translated from `Question_Eng`, `Context_Eng`, `Answer_Eng`

- First, Check content of `Context` and collate with `Context_Eng`. If content reasionable, please not edit; else Edit at `Edit_ConText`


- Second, Use the slider bar to change the content 

<img width="964" alt="interface" src="https://github.com/autobotasia/ViQuAD/blob/master/images/silde_bar_1.PNG?raw=true">

- And save at textarea of `Edit Answer`

<img width="964" alt="interface" src="https://github.com/autobotasia/ViQuAD/blob/master/images/edit_answer_1.PNG?raw=true">

- collate with the answers highlighted in `Context_Eng`:

<img width="964" alt="interface" src="https://github.com/autobotasia/ViQuAD/blob/master/images/context_eng_1.png?raw=true">

- 
