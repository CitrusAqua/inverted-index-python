import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
import os
import json
import math

document_file = 'data.CSV'
temp_path = 'temp/'
docname_file = 'docname.json'
doc_word_file = 'doc_word.json'
doc_tf_file = 'doc_tf.json'
word_idf_file = 'word_idf.json'
tf_idf_file = 'tf_idf.json'
tf_idf_abs_file = 'tf_idf_abs.json'
inverted_index_file = 'inverted_index.json'

def _abs(e):
    sum = 0
    for v in e.values():
        sum += v*v
    return math.sqrt(sum)

def gettf(f):
    if f == 0:
        return 0
    return 1 + math.log(f, 10)

if __name__ == '__main__':

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    tokenizer = RegexpTokenizer(r'\w+')
    docname = {}

    doc_word = []
    doc_tf = []
    word_idf = dict()
    tf_idf = []

    with open(document_file, encoding='utf-8') as csvfile:
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

            doc_word.append(word_dict)

            tf_dict = {k: gettf(v) for k, v in word_dict.items()}
            doc_tf.append(tf_dict)

            docname[count] = row[0]

            count += 1

    for i in range(count):
        tf_idf_dict = dict()
        for k in doc_tf[i]:
            if k not in word_idf:
                ni = 0
                for item in doc_word:
                    if k in item:
                        ni += 1
                idf = math.log(count/ni, 10)
                word_idf[k] = idf
            tf_idf_dict[k] = word_idf[k] * idf
        tf_idf.append(tf_idf_dict)

    tf_idf_abs = [_abs(e) for e in tf_idf]


    with open(docname_file, 'wb') as thisfile:
        thisfile.write(json.dumps(docname).encode('utf-8'))

    with open(doc_word_file, 'wb') as thisfile:
        thisfile.write(json.dumps(doc_word).encode('utf-8'))

    with open(doc_tf_file, 'wb') as thisfile:
        thisfile.write(json.dumps(doc_tf).encode('utf-8'))

    with open(word_idf_file, 'wb') as thisfile:
        thisfile.write(json.dumps(word_idf).encode('utf-8'))

    with open(tf_idf_file, 'wb') as thisfile:
        thisfile.write(json.dumps(tf_idf).encode('utf-8'))

    with open(tf_idf_abs_file, 'wb') as thisfile:
        thisfile.write(json.dumps(tf_idf_abs).encode('utf-8'))


    invindex = dict()
    files= os.listdir(temp_path)

    count = 0
    for data in doc_word:
        for key in data:
            if key not in invindex:
                invindex[key] = [count]
            else:
                invindex[key].append(count)
        count += 1

    with open(inverted_index_file, 'wb') as f:
        f.write(json.dumps(invindex).encode('utf-8'))