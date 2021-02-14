
file = open( "source.txt", "r")
lines = file.readlines()
file.close()

outputlines = []
for line in lines:
	split_line = line.split(' • ')
	outputlines.append(split_line[0]+'\n')




with open('new_source.txt', 'w') as f:
    for item in outputlines:
        f.write("%s" % item)

#string = "the •  word"
