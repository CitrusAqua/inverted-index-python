import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
import os
import json

document_file = 'data.CSV'
temp_path = 'temp/'
docname_file = 'docname.json'
inverted_index_file = 'inverted_index.json'

if __name__ == '__main__':
    
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

    invindex = dict()
    files= os.listdir(temp_path)
    for file in files:
        fname = file.split('.')[0]
        f = open(temp_path + file)
        data = json.load(f)
        f.close()
        for key in data:
            if key not in invindex:
                invindex[key] = [int(fname)]
            else:
                invindex[key].append(int(fname))

	# for k in invindex:
	# 	invindex[k].sort()

    with open(inverted_index_file, 'wb') as f:
        f.write(json.dumps(invindex).encode('utf-8'))