
import re
file = open( "source.txt", "r")
lines = file.readlines()
file.close()



outputlines = []
for line in lines:
	#split_line = line.split('	')
	for n in re.findall(r'[\u4e00-\u9fff]+', line):
		outputlines.append(n)


with open('new_source.txt', 'w') as f:
    for item in outputlines:
        f.write("%s" % item+'\n')

#string = "the •  word"
