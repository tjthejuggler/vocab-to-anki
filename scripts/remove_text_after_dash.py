from os import path

lang = 'tr'
file = open( "script_source.txt", "r")
lines = file.readlines()
file.close()

swappedlines = []
swappedlines.append(lines[0])
swappedlines.append(lines[1])
for linenumber in range (2,len(lines)):
	print(linenumber)
	if ' - ' in lines[linenumber]:
		split_line = lines[linenumber].split(' - ')
		swappedlines.append('')
		swappedlines[linenumber] = split_line[0] + '\n'
		print('split_line', split_line)
	else:
		swappedlines.append('')
		swappedlines[linenumber] = lines[linenumber]  + '\n'

with open('new_source.txt', 'w') as f:
    for item in swappedlines:
        f.write("%s" % item)