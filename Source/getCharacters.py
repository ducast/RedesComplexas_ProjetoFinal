import bisect
import codecs
import numpy as np
import os
import re
import string
import sys
import graph_tool.all

def getHighestVertex (graph, vertices):
	max_degree = -1
	highest = vertices[0]
	for index in vertices:
		v = graph.vertex(index)
		if v.out_degree() > max_degree:
			max_degree = v.out_degree()
			highest = index
	return highest

# def drawGraph(oldG, oldSize, index, graphicIndex):
# 	g = graph_tool.Graph(oldG)
# 	notUsedCharacters = [i for i in g.vertices() if g.vertex(i).in_degree()+g.vertex(i).out_degree() == 0]
# 	g.remove_vertex(notUsedCharacters)
# 	namesProp = oldG.vertex_properties['name'].a
# 	newNamesProp = [n for n in namesProp if namesProp.index(n) not in ]

# 	graphSize = len([i for i in g.vertices()])
# 	if graphSize > oldSize:
# 		deg = g.degree_property_map("total")
# 		names = g.vertex_properties['name']
# 		deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
# 		pos = graph_tool.draw.sfdp_layout(g)
# 		control = g.new_edge_property("vector<double>")
# 		for e in g.edges():
# 			d = np.sqrt(sum((pos[e.source()].a - pos[e.target()].a) ** 2)) / 5
# 			control[e] = [0.3, d, 0.7, d]
# 		graph_tool.draw.graph_draw(g, pos=pos, vertex_size=deg, vertex_fill_color=deg, vorder=deg, vertex_text=names,
# 						output="../Images/GraphSelfies/HP_book{}-draw{}.pdf".format(index, graphicIndex))
# 	return graphSize

if __name__ == '__main__':
	# Reading characters list
	f=open('../Lib/parsedHPcharacters-final.txt')
	characters = f.readlines()
	f.close()

	# Creating empty graph and its properties
	blank_graph = graph_tool.Graph(directed=False)
	blank_graph.vertex_properties['name']  = blank_graph.new_vertex_property("string")
	blank_graph.edge_properties['weight']  = blank_graph.new_edge_property("double")

	# Writing characters map file and adding them to the graph
	characters.sort()
	oldCharacters = [c.replace('\n', '') for c in characters]
	f=open('../Lib/charactersMap.txt','w')
	for c in range(len(characters)):
		v = blank_graph.add_vertex()
		blank_graph.vertex_properties['name'][v]  = characters[c].replace('\n', '')
		f.write("%d "%c + characters[c])
		characters[c] = characters[c][:-1].split(" ")
	f.close()

	# Adding relations
	booksDir = "../Books/HarryPotter"
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]
	exceptions = ['Mr','Mrs','Sr','Jr']
	for book in booksPaths:
		g = graph_tool.Graph(blank_graph)
		k = booksPaths.index(book)
		toPrint = False
		# graficIndex = 0
		# graphSize = 0
		usedCharacters = []
		with codecs.open(book, 'r', 'utf-8') as bookFile:
			last_word = False
			pageCharacters = []
			for line in bookFile:
				if 'Page |' in line: # New page
					# Removing repeated characters
					pageCharacters = np.unique(pageCharacters)
					usedCharacters+=pageCharacters.tolist()
					for i, c1 in enumerate(pageCharacters):
						for c2 in pageCharacters[(i+1):]:
							v1 = g.vertex(c1)
							v2 = g.vertex(c2)
							myEdge = g.edge(v1, v2)
							if myEdge == None:	# New edge
								newEdge = g.add_edge(v1, v2)
								g.edge_properties['weight'][newEdge] = 1
							else:
								g.edge_properties['weight'][myEdge] += 1
						# graphSize = drawGraph(g, graphSize, k+1, graficIndex)
						# if graphSize > 5:
						# 	break
						# graficIndex+=1
					pageCharacters = []

				else:
					lineWords = re.compile('\w+-*').findall(line)
					for word in lineWords:
						if word[0].isupper():
							count = 0
							indexes = []
							if last_word:  # In case of Name conflict, or Mr., Mrs.
								for char in characters:
									if word in char and last_word in char:
										count+=1
										indexes.append(characters.index(char))
								if count == 0: # In case they don't match
									if last_word not in exceptions:
										pageCharacters.append(highest)
										last_indexes = []
										last_word = False
									for char in characters:
										if word in char:
											count+=1
											indexes.append(characters.index(char))
							else: # Check if word matches a character
								for char in characters:
									if word in char:
										count+=1
										indexes.append(characters.index(char))

							if word in exceptions or count > 1:
								last_word = word
								last_indexes = indexes
								indexes = []
							else:
								last_word = False
								last_indexes = []

							if len(indexes) == 1:
								if indexes[0] not in pageCharacters:
									pageCharacters.append(indexes[0])
						else:
							if len(last_indexes) == 1:
								pageCharacters.append(last_indexes[0])
							elif len(last_indexes) > 1:
								highest = getHighestVertex(g,last_indexes)
								pageCharacters.append(highest)
							last_word = False
							last_indexes = []


		# Removing characters that didnt apear in this book
		usedCharacters = np.unique(usedCharacters).tolist()
		for c in oldCharacters:
			if oldCharacters.index(c) not in usedCharacters:
				v = [i for i in g.vertices() if g.vertex_properties['name'][i] == c]
				g.remove_vertex(v)

		g.save('../Networks/CharacterNetworks/HP_book{}.gml'.format(k+1))

