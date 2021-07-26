from difflib import SequenceMatcher
from os import path
import os
import json
import re
from pathlib import Path
from num2words import num2words
from translation_helper import *

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()

def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def add_apostrophe_if_needed(word, lang):
	to_return = word
	if lang == 'en':
		file = word+'.mp3'
		local_dict_file = 'apos_previously_changed.json'
		if path.exists(cwd+'/scripts/'+local_dict_file):			
			with open(cwd+'/scripts/'+local_dict_file) as json_file:
				local_dict = json.load(json_file)
				if file in local_dict:
					to_return = local_dict[file].replace(".mp3","")
	return to_return

def clean_string(line):
	line = line.strip('\n')
	line = ' '.join(s for s in line.split() if not any(c.isdigit() for c in s)) #remove digits from string
	line = line.lower()
	return line

def remove_special_characters(line):
	return re.sub(r"[^\w\d'\s]",'',line)

def remove_special_characters_and_add_apostrophes(line, lang):
	line = remove_special_characters(line)
	for word in line.split():
		line = line.replace(word, add_apostrophe_if_needed(word, lang))
	return line

def get_hint_from_formatted_line(split_line):
	hint = ""
	if len(split_line) > 2:
		hint = split_line[2]
	return hint

def convert_numbers_to_words(words, lang):
	#print('lang', lang)
	converted_words = ''
	for word in words.split():
		word_to_add = word
		if word.isdecimal():
			word = int(word)
			try:
				word_to_add = num2words(word, lang=lang)
			except NotImplementedError:
				word_to_add = get_translation(num2words(word, lang='en'), 'en', lang)
		if converted_words == '':
			converted_words = word_to_add
		else:
			converted_words += ' ' + word_to_add
	return converted_words