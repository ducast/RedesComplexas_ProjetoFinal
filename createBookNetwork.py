import codecs
from graph_tool.all import *
import numpy as np
import os
import re
import string
import sys

if __name__ == '__main__':
	booksDir = sys.argv[1]
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]
	lines = []
	# for book in booksPaths:
	# words = []
	# with codecs.open(booksPaths[0], 'r', 'utf-8') as bookFile:
	# 	for line in bookFile:
	# 		if 'Page |' not in line: # Dont consider page end
	# 			lineWords = re.compile('\w+').findall(line)
	# 			if len(lineWords) > 0 :
	# 				words += lineWords

	# uniqueWords, wordsCount = np.unique(words, return_counts=True)
	# index = []
	# for w, c in zip(uniqueWords, wordsCount):
	# 	if w.isdigit():
	# 		index.append(np.argwhere(uniqueWords==w))
	# uniqueWords = np.delete(uniqueWords, index)
	# wordsCount = np.delete(wordsCount, index)

	g = graph_tool.Graph()
	g.vertex_properties['count'] = g.new_vertex_property("double")
	g.vertex_properties['name'] = g.new_vertex_property("string")
	g.edge_properties['weight'] = g.new_edge_property("double")
	with codecs.open(booksPaths[0], 'r', 'utf-8') as bookFile:
		for line in bookFile:
			if 'Page |' not in line: # Dont consider page end
				lineWords = re.compile('\w+').findall(line)
				lineWords = [w.lower() for w in lineWords]
				if len(lineWords) > 0:
					for i, word in enumerate(lineWords):
						if (i+1) == len(lineWords):
							break
						next_word = lineWords[i + 1]
						myVertex = g.vertices()
						vertexNames = [g.vertex_properties['name'][v] for v in myVertex]
						wordIndex = [i for i in myVertex if i['name']==word]
						nextWordIndex = [i for i in myVertex if i['name']==next_word]
						
						if len(wordIndex) == 0:
							v = g.add_vertex()
							g.vertex_properties['count'][v] = 1
						else:
							v = g.vertex(wordIndex[0])
							g.vertex_properties['count'][wordIndex] += 1
						
						if len(nextWordIndex) == 0:
							nextV = g.add_vertex()
							g.vertex_properties['count'][nextV] = 0
						else:
							nextV = g.vertex(nextWordIndex[0])

						myEdge = g.edge(v, nextV)
						if myEdge == None:
							newEdge = g.add_edge(v, nextV)
							g.edge_properties['weight'][newEdge] = 1
						else:
							g.edge_properties['weight'][myEdge] += 1


	