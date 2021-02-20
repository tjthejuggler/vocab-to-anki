from os import path

lang = 'tr'
file = open( "source.txt", "r")
lines = file.readlines()
file.close()

formated_lines = []

for linenumber in range (0,len(lines)):
	split_line = lines[linenumber].split()
	word = split_line[1]
	print(word)
	#formated_line = split_line[1] + ' - ' + split_line[2] + ' - no hint\n'
	formated_lines.append(word)


with open('commonwords_formated.txt', 'w') as f:
    for item in formated_lines:
        f.write("%s" % item+'\n')

