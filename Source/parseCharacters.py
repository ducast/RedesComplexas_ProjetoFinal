f=open('../Lib/HPcharactersWikipedia.txt')
lines = f.readlines()
f.close()
characters = []
for line in lines:
    if '*[[' in line:
        end = line.index(']]')
        character = line[3:end]
        if "|" in character:
            start = character.index("|")+1
            character = character[start:]
        characters.append(character)
out = '\n'.join(characters)
f=open('../Lib/parsedHPcharacters.txt','w')
f.write(out)
f.close()
