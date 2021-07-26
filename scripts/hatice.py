import os
from os import path
from pathlib import Path
#import json
from google.cloud import translate_v2 as translate
import six
import re
target_language = 'it'

def translate_text(text):
	translate_client = translate.Client()
	if isinstance(text, six.binary_type):
		text = text.decode("utf-8")
	result = translate_client.translate(text, target_language=target_language)
	return(format(result["translatedText"]))

def main():
	file = open( "script_source.txt", "r")
	lines = file.readlines()
	file.close()
	outputlines = []
	for line in lines:
		print('line', line)
		line = line.strip()
		new_line = ''
		if len(re.findall('"', line)) == 2:
			in_between_quotes = re.findall('"([^"]*)"', line)[0]
			alpha_count = 0
			for char in in_between_quotes:
				if char.isalpha():
					alpha_count += 1
			print('alpha_count', alpha_count)
			if alpha_count > 1:				 
				translated_in_between_quotes = translate_text(in_between_quotes)
				new_line = line.replace('"'+in_between_quotes+'"', '"'+translated_in_between_quotes+'"')
			else:
				new_line = line
		else:
			new_line = line
		print('new_line', new_line)
		outputlines.append(new_line)
	with open('new_source.txt', 'w') as f:
	    for item in outputlines:
	        f.write("%s" % item+'\n')

main()