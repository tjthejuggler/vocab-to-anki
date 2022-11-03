import os
from os import path
from pathlib import Path
#import json
from google.cloud import translate_v2 as translate
import six
import re
target_language = 'it'

def has_more_than_n_words(num, words):
	word_list = words.split()
	return len(word_list) > num

def main():
	file = open( "script_source.txt", "r")
	lines = file.readlines()
	file.close()
	outputlines = []
	new_line = ''
	should_send_line = False
	for line in lines:
		line = re.sub(r"[^\w\d'\s]",'',line)
		print('line', line)
		line = line.strip()
		if line:
			new_line = new_line + line + ' '
		else:
			should_send_line = True 
		if re.match('[?.!]$', line):
			should_send_line = True
		if should_send_line:
			print('new_line', new_line)
			if has_more_than_n_words(2,new_line):
				outputlines.append(new_line)
			new_line = ''
	outputlines = list(set(outputlines))
	with open('new_source.txt', 'w') as f:
	    for item in outputlines:
	        f.write("%s" % item+'\n')

main()