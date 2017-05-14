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

	g = graph_tool.Graph()
	g.vertex_properties['count'] = g.new_vertex_property("double")
	g.vertex_properties['name'] = g.new_vertex_property("string")
	g.edge_properties['weight'] = g.new_edge_property("double")

	for i, bookPath in enumerate(booksPaths):
		with codecs.open(booksPaths, 'r', 'utf-8') as bookFile:
			for line in bookFile:
				if 'Page |' not in line: # Dont consider page end
					lineWords = re.compile('\w+').findall(line)
					lineWords = [w.lower() for w in lineWords]
					if len(lineWords) > 0: # Dont consider empty line
						for i, word in enumerate(lineWords):
							if (i+1) == len(lineWords): #Last word of the sentence
								next_word = None
							else:
								next_word = lineWords[i + 1]
							wordIndex = [i for i in g.vertices() if g.vertex_properties['name'][i] == word]
							nextWordIndex = [i for i in g.vertices() if g.vertex_properties['name'][i] == next_word]

							if len(wordIndex) == 0:
								v = g.add_vertex()
								g.vertex_properties['count'][v] = 1
								g.vertex_properties['name'][v] = word
							else:
								v = g.vertex(wordIndex[0])
								g.vertex_properties['count'][wordIndex[0]] += 1
							
							if next_word != None:
								if len(nextWordIndex) == 0:
									nextV = g.add_vertex()
									g.vertex_properties['count'][nextV] = 0
									g.vertex_properties['name'][nextV] = next_word
								else:
									nextV = g.vertex(nextWordIndex[0])

							myEdge = g.edge(v, nextV)
							if myEdge == None:
								newEdge = g.add_edge(v, nextV)
								g.edge_properties['weight'][newEdge] = 1
							else:
								g.edge_properties['weight'][myEdge] += 1

	for v in g.vertices():
		print (g.vertex_properties['name'][v], g.vertex_properties['count'][v])

	g.save('HP_book{}.gml'.format(i))


	