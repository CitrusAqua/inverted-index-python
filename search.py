import sys
import json
import time


inverted_index_file = 'inverted_index.json'
docname_file = 'docname.json'

if __name__ == '__main__':

	start = time.time()

	docf = open(docname_file)
	docdata = json.load(docf)
	docf.close()

	f = open(inverted_index_file)
	data = json.load(f)
	f.close()

	curpos = 0
	flag_not = False
	doc_count = len(docdata)
	filtered = [range(doc_count)]
	for arg in sys.argv[1:]:
		if arg == 'or':
			curpos += 1
			filtered.append(range(doc_count))
			continue
		if arg == 'not':
			flag_not = True
			continue
		if flag_not:
			if arg in data:
				filtered[curpos] = [i for i in filtered[curpos] if i not in data[arg]]
			flag_not = False
			continue
		if arg in data:
			filtered[curpos] = [i for i in filtered[curpos] if i in data[arg]]
		else:
			filtered[curpos] = []
			break

	union = set()
	for ls in filtered:
		for e in ls:
			union.add(e)


	end = time.time()
	elp = end - start
	elp_ms = elp * 1000

	print('')
	print('---------Search Result---------')
	print(len(union), 'result(s) got in ', format(elp_ms, '.3f'), 'ms')
	print('')

	for i in union:
		print(i, docdata[str(i)])

	print('')