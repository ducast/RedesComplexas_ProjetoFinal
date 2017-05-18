import bisect
import codecs
import numpy as np
import os
import re
import string
import sys

if __name__ == '__main__':
	f=open('../Lib/1000commonWords.txt')
	words = f.readlines()
	f.close()
	words.sort()
	booksDir = "../Books"
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]
	lines = []
	for book in booksPaths:
		uppers = []
		with codecs.open(book, 'r', 'utf-8') as bookFile:
			for line in bookFile:
				if 'Page |' not in line: # Dont consider page end
					lineWords = re.compile('\w+').findall(line)
					for w in lineWords:
						if w[0].isupper():
							uppers.append(w)
			uniqueUppers, uppersCount = np.unique(uppers, return_counts=True)
			characters = []
			for word in uniqueUppers:
				w = word.lower()
				i = bisect.bisect_left(words,w)
				if i < len(words) and words[i] == w+'\n':
					pass
				else:
					characters.append(word)
					print word
