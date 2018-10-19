import os
import json

temp_path = 'temp/'
inverted_index_file = 'inverted_index.json'

def reduce():
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