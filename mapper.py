import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
import os
import json

document_file = 'data.CSV'
temp_path = 'temp/'
docname_file = 'docname.json'

def map():

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    tokenizer = RegexpTokenizer(r'\w+')
    docname = {}

    with open(document_file) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            word_dict = dict()
            for col in row:
                disease_list = tokenizer.tokenize(col)
                lower_list = [w.lower() for w in disease_list]
                filtered = [w for w in lower_list if w not in stopwords.words('english')]
                Rfiltered = nltk.pos_tag(filtered)
                for element in Rfiltered:
                    raw_word = element[0]
                    if raw_word not in word_dict:
                        word_dict[raw_word] = 1
                    else:
                        word_dict[raw_word] += 1

            tpath = os.path.join(temp_path, str(count)+'.json')
            with open(tpath, 'wb') as tmpf:
                tmpf.write(json.dumps(word_dict).encode('utf-8'))

            docname[count] = row[0]

            count += 1

    with open(docname_file, 'wb') as dcnf:
        dcnf.write(json.dumps(docname).encode('utf-8'))