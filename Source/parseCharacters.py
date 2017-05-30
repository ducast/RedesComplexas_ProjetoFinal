f=open('../Lib/HPcharactersWikipedia.txt')
lines = f.readlines()
f.close()
characters = []
for line in lines:
	if '*' in line:
		if '[[' in line[:5]:
			end = line.index(']]')
			start = line.index('[[')+2
			character = line[start:end]
		else:
			end = line.index(' \xe2')
			character = line[1:end]
		if "|" in character:
			start = character.index("|")+1
			character = character[start:]
		characters.append(character)
out = '\n'.join(characters)
f=open('../Lib/parsedHPcharacters2.txt','w')
f.write(out)
f.close()
