#loop each line, add it to list if it does not
#	contain a number
#	be blank
#	already exists
#add every unique word from every item in list to new list
#combine the lists

from os import path

file = open( "script_source.txt", "r")
lines = file.readlines()
file.close()

saved_lines = []
# swappedlines = []
# swappedlines.append(lines[0])
# swappedlines.append(lines[1])
for line in lines:
	use_this_line = True
	if not line.strip():
		continue
	if line in saved_lines:
		continue
	for char in line:
		if char.isdigit():
			use_this_line = False
			continue
	if use_this_line:
		saved_lines.append(line)

saved_words = []
for saved_line in saved_lines:
	print('line', saved_line)
	for word in saved_line.split():
		print('word', word)
		if not (word+"\n") in saved_words:
			saved_words.append(word+"\n")
full_list = saved_lines + saved_words


	# if ' - ' in lines[linenumber]:
	# 	split_line = lines[linenumber].split(' - ')
	# 	swappedlines.append('')
	# 	swappedlines[linenumber] = split_line[0] + '\n'
	# 	print('split_line', split_line)
	# else:
	# 	swappedlines.append('')
	# 	swappedlines[linenumber] = lines[linenumber]  + '\n'

with open('new_source.txt', 'w') as f:
    for item in full_list:
        f.write("%s" % item)