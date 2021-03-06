import codecs
from graph_tool.all import *
import numpy as np
import os
import re
import string
import sys

if __name__ == '__main__':
	booksDir   = sys.argv[1]
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]

	for k, bookPath in enumerate(booksPaths):
		print bookPath
		g = graph_tool.Graph()
		g.vertex_properties['count'] = g.new_vertex_property("double")
		g.vertex_properties['name']  = g.new_vertex_property("string")
		g.edge_properties['weight']  = g.new_edge_property("double")
		aux = 0
		with codecs.open(bookPath, 'r', 'utf-8') as bookFile:
			for line in bookFile:
				# Dont consider page end
				if 'Page |' not in line:
					lineWords = re.compile('\w+').findall(line)
					lineWords = [w.lower() for w in lineWords]
					# Dont consider empty line
					if len(lineWords) > 0:
						for i, word in enumerate(lineWords):
							#Last word of the sentence
							if (i+1) == len(lineWords):
								next_word = None
							else:
								next_word = lineWords[i + 1]
							
							wordIndex     = [i for i in g.vertices() if g.vertex_properties['name'][i] == word]
							nextWordIndex = [i for i in g.vertices() if g.vertex_properties['name'][i] == next_word]

							if len(wordIndex) == 0:
								v = g.add_vertex()
								g.vertex_properties['count'][v] = 1
								g.vertex_properties['name'][v]  = word
							else:
								v = g.vertex(wordIndex[0])
								g.vertex_properties['count'][wordIndex[0]] += 1
							
							if next_word != None:
								if len(nextWordIndex) == 0:
									nextV = g.add_vertex()
									g.vertex_properties['count'][nextV] = 0
									g.vertex_properties['name'][nextV]  = next_word
								else:
									nextV = g.vertex(nextWordIndex[0])

								myEdge = g.edge(v, nextV)
								if myEdge == None:
									newEdge = g.add_edge(v, nextV)
									g.edge_properties['weight'][newEdge] = 1
								else:
									g.edge_properties['weight'][myEdge] += 1

							aux+=1
							if aux%1000 == 0:
								print(aux)

		g.save('HP_book{}.gml'.format(k+3))

	# for v in g.vertices():
	# 	print (g.vertex_properties['name'][v], g.vertex_properties['count'][v])


	