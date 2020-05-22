

import time
from googletrans import Translator
#from googletrans.gtoken import TokenAcquirer
translator = Translator()
#acquirer = TokenAcquirer()
#text = 'test'
#tk = acquirer.do(text)

#print(tk)
datafile = open('fileout_dev.txt','r',encoding="utf-8")
#for j in range(0,21249):
#    text = datafile.readline()
with open('file_translate_dev.txt','w',encoding = 'utf-8') as fileout:
    for i in range(0,2474+1):
        text = datafile.readline()
        senten = translator.translate(text,dest='vi').text
        texts = senten + '\n' 
        fileout.write(texts)
        print(i)
        time.sleep(2)