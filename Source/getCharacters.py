import bisect
import codecs
import numpy as np
import os
import re
import string
import sys

if __name__ == '__main__':
	f=open('../Lib/parsedHPcharacters.txt')
	characters = f.readlines()
	f.close()
	characters.sort()
	f=open('../Lib/charactersMap.txt','w')
	blank_graph = graph_tool.Graph()
	blank_graph.vertex_properties['name']  = blank_graph.new_vertex_property("string")
	for c in range(len(characters)):
		v = blank_graph.add_vertex()
		blank_graph.vertex_properties['name'] = char
		f.write("%d "%c + characters[c])
		characters[c] = characters[c][:-1].split(" ")
	f.close()
	booksDir = "../Books/HarryPotter"
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]
	exceptions = ['Mr','Mrs','Sr','Jr']
	for book in booksPaths[:1]:
		g = Graph(blank_graph)
		with codecs.open(book, 'r', 'utf-8') as bookFile:
			last_word = False
			pageCharacters = []
			for line in bookFile:
				if 'Page |' in line: # New page
					for c1 in pageCharacters:
						for c2 in pageCharacters:
							if c1 != c2:
								v1 = g.vertex(c1)
								v2 = g.vertex(c2)
								g.add_edge(v1, v2)
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
										pass # TODO: last -> highest
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
								last = False
								last_indexes = []
							if len(indexes) == 1:
								if indexes[0] not in pageCharacters:
									pageCharacters.append(indexes[0])
							elif len(indexes) > 1:
								pass #TODO: last->highest
						else:
							last = False
							last_indexes = []
