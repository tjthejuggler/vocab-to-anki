apos_words = [
"I'm",
"I'd",
"it's",
"I've",
"he's",
"I'll",
"he'd",
"we'd",
"it'd",
"don't",
"can't",
"we're",
"isn't",
"won't",
"we've",
"we'll",
"she's",
"you'd",
"let's",
"who's",
"he'll",
"it'll",
"she'd",
"ain't",
"who'd",
"that's",
"didn't",
"you're",
"you'll",
"what's",
"wasn't",
"you've",
"aren't",
"here's",
"hasn't",
"hadn't",
"they'd",
"here's",
"who've",
"she'll",
"who'll",
"that'd",
"doesn't",
"there's",
"they're",
"world's",
"haven't",
"they've",
"weren't",
"they'll",
"o'clock",
"mustn't",
"needn't",
"must've",
"that'll",
"couldn't",
"wouldn't",
"could've",
"would've",
"there'll",
"shouldn't",
"should've"
]

import os
from os import path
from pathlib import Path
from os import listdir
from os.path import isfile, join
import re
import shutil
import json
#this is a script that renames all files in a directory to lowercase

cwd = os.getcwd()
home = str(Path.home())
pron_fold = home+'/pronunciations'
lang = 'en'
parent_dir = pron_fold+'/'+lang+'/'

def addToAutoChangedList(word):
      lines=''
      try:
            file = open(cwd+"/apos_auto_changed.txt", "r")
            lines = file.read()
            file.close()

      except:
            #print("file doesn't exist", word)
            pass
      lines = lines + ("\n"+word)
      text_file = open(cwd+"/apos_auto_changed.txt", "w")
      text_file.write(lines)
      text_file.close()

def addToPreviosulySkipped(word):
      lines=''
      try:
            file = open(cwd+"/apos_previously_skipped.txt", "r")
            lines = file.read()
            file.close()

      except:
            #print("file doesn't exist", word)
            pass
      lines = lines + ("\n"+word)
      text_file = open(cwd+"/apos_previously_skipped.txt", "w")
      text_file.write(lines)
      text_file.close()

def has_been_previously_skipped(word):
	to_return = False
	#local_dict_file, swapped = get_local_dictionary(second_lang,first_lang)
	file = open("apos_previously_skipped.txt", "r")
	lines = file.readlines()
	file.close()
	lines = [x.strip() for x in lines]
	print('word', word)
	print('lines', lines)
	if word in lines:
		to_return = True
	return to_return	

def add_to_previously_changed_and_kept(word):
      lines=''
      try:
            file = open(cwd+"/apos_previously_changed_and_kept.txt", "r")
            lines = file.read()
            file.close()

      except:
            #print("file doesn't exist", word)
            pass
      lines = lines + ("\n"+word)
      text_file = open(cwd+"/apos_previously_changed_and_kept.txt", "w")
      text_file.write(lines)
      text_file.close()

def has_been_previously_changed_and_kept(word):
	to_return = False
	#local_dict_file, swapped = get_local_dictionary(second_lang,first_lang)
	file = open("apos_previously_changed_and_kept.txt", "r")
	lines = file.readlines()
	file.close()
	if word in lines:
		to_return = True
	return to_return

def get_change_all_words_from_file():
	file = open("apos_change_all_words.txt", "r")
	lines = file.readlines()
	file.close()
	lines = [x.strip() for x in lines]
	return lines	

def update_change_all_words_file(word):
      lines=''
      try:
            file = open(cwd+"/apos_change_all_words.txt", "r")
            lines = file.read()
            file.close()
      except:
            pass
      lines = lines + ("\n"+word)
      text_file = open(cwd+"/apos_change_all_words.txt", "w")
      text_file.write(lines)
      text_file.close()

def get_previously_changed(file):
	to_return = ''
	local_dict_file = 'apos_previously_changed.json'
	if path.exists(cwd+'/'+local_dict_file):			
		with open(cwd+'/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if file in local_dict:
				to_return = local_dict[file]
	return to_return

def save_rename_pair_to_file(old_name, new_name):
	local_dict_file = 'apos_previously_changed.json'
	local_dict = {}
	if path.exists(cwd+'/'+local_dict_file):			
		with open(cwd+'/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
	if not old_name in local_dict:
		local_dict[old_name] = new_name
		my_json = json.dumps(local_dict)
		f = open(cwd+'/'+local_dict_file,"w")
		f.write(my_json)
		f.close()

def rename_file(old_name, new_name):
	print('renam', old_name, new_name)
	os.rename(parent_dir+old_name, parent_dir+new_name)
	save_rename_pair_to_file(old_name, new_name)

def create_new_file(old_name, new_name):
	chunks_folder_name = cwd+"/Learn Turkish - Word Power 101 - "+"{0:0=2d}".format(folder_num)+"chunks/"
	chunks_file_name = "wp1010"+str(folder_num)+"chunk"+str(file_num_to_name)+".mp3"
	src = chunks_folder_name + chunks_file_name
	dst = cwd+"/"+language+"/"+name+".mp3"
	shutil.copy(src,dst)

onlyfiles = [f for f in listdir(parent_dir) if isfile(join(parent_dir, f))]

without_apos_words = []

for apos_word in apos_words:
	without_apos_words.append(re.sub(r'[^\w\s]','',apos_word))

#change_all_words = ["dont","youre","Im"]
changed_automatically = []

for file in onlyfiles:
	change_all_words = get_change_all_words_from_file()
	already_dealt_with = False
	if has_been_previously_skipped(file):
		print("has been previously skipped", file)
		already_dealt_with = True
	if already_dealt_with == False and has_been_previously_changed_and_kept(file):
		shutil.copy(parent_dir+file, parent_dir+get_previously_changed(file))
		already_dealt_with = True
	if already_dealt_with == False and get_previously_changed(file) != '':
		rename_file(file, get_previously_changed(file))
		already_dealt_with = True
	for change_all_word in change_all_words:
		#if (change_all_word+" ") in file:
		if re.search(r'\b' + change_all_word + r'\b', file):
			print('fff',file,change_all_word)
			index = without_apos_words.index(change_all_word)
			rename_file(file, file.replace(change_all_word,apos_words[index]))
			addToAutoChangedList(file.replace(change_all_word,apos_words[index]))
			print("change all", file, file.replace(change_all_word,apos_words[index]))
			print("\n")
			already_dealt_with = True
			break
	if already_dealt_with == False:
		for without_apos_word in without_apos_words:
			index = without_apos_words.index(without_apos_word)
			if re.search(r'\b' + without_apos_word + r'\b', file):
				print(file, ":", without_apos_word)
				val = input("1)change       2)change all       3)leave as is      4)change and keep") 
				if val == "1":
					rename_file(file, file.replace(without_apos_word,apos_words[index]))
					#os.rename(file, file.replace(without_apos_word,apos_words[index]))
					print("1", file, file.replace(without_apos_word,apos_words[index]))
					print("\n")
				if val == "2":
					rename_file(file, file.replace(without_apos_word,apos_words[index]))
					#os.rename(parent_dir+file, parent_dir+file.replace(without_apos_word,apos_words[index]))
					#change_all_words.append(without_apos_word)
					update_change_all_words_file(without_apos_word)
					print("1", file, file.replace(without_apos_word,apos_words[index]))
					print(change_all_words)
					print("\n")
				if val == "3":
					addToPreviosulySkipped(file)
					print("dont change", file)
					print("\n")
				if val == "4":
					print('change and keep', file, file.replace(without_apos_word,apos_words[index]))
					shutil.copy(parent_dir+file, parent_dir+file.replace(without_apos_word,apos_words[index]))
					save_rename_pair_to_file(file, file.replace(without_apos_word,apos_words[index]))
					add_to_previously_changed_and_kept(file)