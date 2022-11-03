from os import path

file = open( "script_source.txt", "r")
lines = file.readlines()
file.close()

formated_lines = []

for line in lines:
	split_line = line.split()
	for item in split_line:
		if item.isdecimal():
			item = '\n' + item + ' '
		formated_lines.append(item)



with open('script_source_output.txt', 'w') as f:
    for item in formated_lines:
        f.write("%s" % item)

