import codecs
import sys
import os
import re
import numpy as np

def getWords(l):
	words = []
	for li in l:
		w = li.split(' ')
		print w
		words += w
	return words

if __name__ == '__main__':
	booksDir = sys.argv[1]
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]
	lines = []
	# for book in booksPaths:
	words = []
	with codecs.open(booksPaths[0], 'r', 'utf-8') as bookFile:
		for line in bookFile:
			if 'Page |' not in line: # Dont consider page end
				lineWords = re.compile('\w+').findall(line)
				if len(lineWords) > 0:
					words += lineWords

	uniqueWords, wordsCount = np.unique(words, return_counts=True)
	print uniqueWords[:10]
	print wordsCount[:10]
	