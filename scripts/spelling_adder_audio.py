from os import path

def get_spelling(word):
	spelled_word = ''
	for char in word:
		if char == 'v':
			char = 'vee'
		spelled_word += char + '. '
	return spelled_word

lang = 'tr'
file = open( "script_source.txt", "r")
lines = file.readlines()
file.close()

newlines = []
for line in lines:
	if ' - ' in line:
		split_line = line.split(' - ')
		spelled_word = get_spelling(split_line[0])
		new_line = split_line[0] + ' - ' + spelled_word + ' - ' + split_line[1].strip() + '\n'
		newlines.append(new_line)

with open('new_source.txt', 'w') as f:
    for item in newlines:
        f.write("%s" % item)