from os import path

lang = 'tr'
file = open( "source.txt", "r")
lines = file.readlines()
file.close()

swappedlines = []
swappedlines.append(lines[0])
swappedlines.append(lines[1])
for linenumber in range (2,len(lines)):
	if ' - ' in lines[linenumber]:
		split_line = lines[linenumber].split(' - ')
		swappedlines.append('')
		swappedlines[linenumber] = split_line[1].rstrip() + ' - ' + split_line[0]
		print('split_line', split_line)
		if len(split_line) > 2:
			swappedlines[linenumber] = swappedlines[linenumber] + ' - ' + split_line[2]
		else:
			swappedlines[linenumber] = swappedlines[linenumber] + ' - no hint\n'

with open('new_source.txt', 'w') as f:
    for item in swappedlines:
        f.write("%s" % item)