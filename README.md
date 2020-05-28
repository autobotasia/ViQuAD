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
