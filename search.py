import sys
import json
import time
import math


inverted_index_file = 'inverted_index.json'
docname_file = 'docname.json'
word_idf_file = 'word_idf.json'
tf_idf_file = 'tf_idf.json'
tf_idf_abs_file = 'tf_idf_abs.json'







def takeSecond(elem):
    return elem[1]

def dot_product(a, b):
	aSet = set(a)
	bSet = set(b)
	_intersection = aSet.intersection(bSet)
	sum = 0
	for e in _intersection:
		sum += a[e] * b[e]
	return sum


if __name__ == '__main__':

	start = time.time()


	f = open(docname_file)
	docdata = json.load(f)
	f.close()

	f = open(inverted_index_file)
	data = json.load(f)
	f.close()


	or_count = 0
	flag_not = False
	doc_count = len(docdata)
	filtered = [range(doc_count)]
	queries = [[]]
	for arg in sys.argv[1:]:

		if arg == 'or':
			or_count += 1
			filtered.append(range(doc_count))
			queries.append([])
			continue

		if arg == 'not':
			flag_not = True
			continue

		if flag_not:
			if arg in data:
				filtered[or_count] = [i for i in filtered[or_count] if i not in data[arg]]
			flag_not = False
			continue

		if arg in data:
			filtered[or_count] = [i for i in filtered[or_count] if i in data[arg]]
			queries[or_count].append(arg)
		else:
			filtered[or_count] = []
			continue


	f = open(word_idf_file)
	word_idf = json.load(f)
	f.close()

	f = open(tf_idf_file)
	tf_idf = json.load(f)
	f.close()

	f = open(tf_idf_abs_file)
	tf_idf_abs = json.load(f)
	f.close()


	res = dict()


	for _iter in range(len(queries)):
		query = queries[_iter]
		weights = dict()
		for word in query:
			tf = 1 + math.log(query.count(word), 10)
			weight = tf * word_idf[word]
			weights[word] = weight

		filtered_with_rel = []
		for v in filtered[_iter]:
			cosine = -1
			if tf_idf_abs[v] != 0:
				# sqrt(sum(Wi,q^2)) is omitted.
				cosine = dot_product(tf_idf[v], weights) / tf_idf_abs[v]
			filtered_with_rel.append((v, cosine))

		for e in filtered_with_rel:
			# res.append(e)
			if e[0] not in res:
				res[e[0]] = e[1]
			else:
				res[e[0]] = max(res[e[0]], e[1])

	# res.sort(key = takeSecond, reverse = True)
	sorted = sorted(res.items(), key = lambda x: x[1], reverse=True)

	end = time.time()
	elp = end - start
	elp_ms = elp * 1000

	print('')
	print('--------------------------Search Result--------------------------')
	print('')
	print('\t', len(res), 'result(s) got in ', format(elp_ms, '.3f'), 'ms')
	print('')

	for i in sorted:
		print('\t', i[0], '\tsim:', "{:0.3f}".format(i[1]), '\t', docdata[str(i[0])])

	print('')