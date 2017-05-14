import codecs
import numpy as np
import os
import re
import string
import sys

if __name__ == '__main__':
	booksDir = sys.argv[1]
	booksPaths = [os.path.join(booksDir, f) for f in os.listdir(booksDir)]
	lines = []
	for book in booksPaths:
		words = []
		with codecs.open(booksPaths[0], 'r', 'utf-8') as bookFile:
			for line in bookFile:
				if 'Page |' not in line: # Dont consider page end
					lineWords = re.compile('\w+').findall(line)
					lineWords = [w.lower() for w in lineWords]
					if len(lineWords) > 0:
						words += lineWords

	uniqueWords, wordsCount = np.unique(words, return_counts=True)

