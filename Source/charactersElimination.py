import bisect
import codecs
import numpy as np
import os
import re
import string
import sys
import graph_tool.all

def getHighestVertex (graph, vertexes):
	max_degree = 0
	highest = None
	for index in vertexes:
		v = graph.vertex(index)
		if v.out_degree() > max_degree:
			max_degree = v.out_degree()
			highest = index
	return index

def createBlank_graph():
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
	f=open('../Lib/charactersMap.txt','w')
	for c in range(len(characters)):
		v = blank_graph.add_vertex()
		blank_graph.vertex_properties['name'][v]  = characters[c].replace('\n', '')
		f.write("%d "%c + characters[c])
		characters[c] = characters[c][:-1].split(" ")
	f.close()

	return blank_graph, characters

def createNetwork(g, characters):
	# Adding relations
	booksDir = "../Books/HarryPotter"
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]
	exceptions = ['Mr','Mrs','Sr','Jr']
	for book in booksPaths:
		with codecs.open(book, 'r', 'utf-8') as bookFile:
			last_word = False
			pageCharacters = []
			for line in bookFile:
				if 'Page |' in line: # New page
					# Removing repeated characters
					pageCharacters = np.unique(pageCharacters)
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
										highest = getHighestVertex(g,last_indexes)
										pageCharacters.append(highest)
									for char in characters:
										if word in char:
											count+=1
											indexes.append(characters.index(char))
							else:
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
							elif len(indexes) > 1:
								highest = getHighestVertex(g,last_indexes)
								pageCharacters.append(highest)
						else:
							if len(last_indexes) == 1:
								pageCharacters.append(last_indexes[0])
							elif len(last_indexes) > 1:
								highest = getHighestVertex(g,last_indexes)
								pageCharacters.append(highest)
							last_word = False
							last_indexes = []

	g.save('../Networks/CharacterNetworks/HP_allBooks.gml')
	return g


if __name__ == '__main__':
	initialGraph, characters = createBlank_graph()
	g = createNetwork(initialGraph, characters)

	#What happens if we eliminate Harry Potter?? Index = 
	

	
