from difflib import SequenceMatcher
from os import path
import os
import json
import re
from pathlib import Path

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()

def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def add_apostrophe_if_needed(word, lang):
	to_return = line
	if lang == 'en'
		file = line+'.mp3'
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