import os
import json
import configparser

def number_docs():
    configParser = configparser.RawConfigParser()   
    configFilePath = r'conf.txt'
    configParser.read(configFilePath)

    document_path = configParser.get('path', 'document_path')
    docnum_filename = configParser.get('filename', 'docnum_file')

    name_dict = dict()
    count = 0
    list_dirs = os.walk(document_path)
    for root, dirs, files in list_dirs:
        for f in files:
            filename = f.split('\\')[-1]
            name_dict[count] = filename
            count += 1

    with open(docnum_filename, 'wb') as docnum_f:
        docnum_f.write(json.dumps(name_dict).encode('utf-8'))