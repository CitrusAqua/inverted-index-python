import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
import os
import json

document_path = 'A:\\Sapphire\\inverted-index-python\\documents\\'
temp_path = 'A:\\Sapphire\\inverted-index-python\\temp\\'


def map():

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    tokenizer = RegexpTokenizer(r'\w+')
    list_dirs = os.walk(document_path)

    for root, dirs, files in list_dirs:
        for f in files:
            word_dict = dict()

            filename = f.split('\\')[-1]
            filename_list = tokenizer.tokenize(filename)
            lower_list = [w.lower() for w in filename_list]
            filtered = [w for w in lower_list if w not in stopwords.words('english')]
            Rfiltered = nltk.pos_tag(filtered)
            for element in Rfiltered:
                word_dict[element[0]] = 1
            
            fpath = os.path.join(root, f)
            with open(fpath, 'rb') as docf:
                for line in docf:
                    disease_list = tokenizer.tokenize(line.decode('utf-8'))
                    lower_list = [w.lower() for w in disease_list]
                    filtered = [w for w in lower_list if w not in stopwords.words('english')]
                    Rfiltered = nltk.pos_tag(filtered)
                    for element in Rfiltered:
                        raw_word = element[0]
                        if raw_word not in word_dict:
                            word_dict[raw_word] = 1
                        else:
                            word_dict[raw_word] += 1

            new_filename = f + '.json'
            tpath = os.path.join(temp_path, new_filename)
            with open(tpath, 'wb') as tmpf:
                tmpf.write(json.dumps(word_dict).encode('utf-8'))