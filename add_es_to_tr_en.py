#input file is formatted
#header
#video
#tr - en - hint
#tr - en - hint
#...

#output file is
#header
#video
#es - tr - en - hint
#tr - en - hint
#...
from deep_translator import (GoogleTranslator,MyMemoryTranslator,QCRI,LingueeTranslator)
import os
from os import path
import json
import time
from googletrans import Translator

translator = Translator()


translator_to_use = 'google'
dest_langcode = 'es'
src_langcode = 'tr'

def add_translation_to_local_dictionary(src_text, dest_text):
	print('add_translation_to_local_dictionary', dest_text)
	cwd = os.getcwd()
	local_dict_file = src_langcode+'_'+dest_langcode+'.json'
	local_dict = {}
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
	if not src_text in local_dict:
		print('!!!',src_text,dest_text)
		local_dict[src_text] = dest_text
		my_json = json.dumps(local_dict)
		f = open(cwd+'/local_dictionaries/'+local_dict_file,"w")
		f.write(my_json)
		f.close()

def translate(src_text):
	global translator_to_use
	print('translator_to_use', translator_to_use)
	print('translate', src_text)
	cwd = os.getcwd()
	local_dict_file = src_langcode+'_'+dest_langcode+'.json'
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]
				print('local dict used', dest_text)
	if dest_text == '':
		if translator_to_use == 'google':
			translator_to_use = 'linguee'
			try:
				print('goog')
				#dest_text = GoogleTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
				dest_text = translator.translate(src_text, src = src_langcode, dest=dest_langcode).text
			except:
				pass			
	if dest_text == '':
		if translator_to_use == 'linguee':
			translator_to_use = 'myMemory'
			try:
				print('lingue')
				dest_text = LingueeTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
			except:
				pass
	if dest_text == '':
		if translator_to_use == 'myMemory':
			translator_to_use = 'pons'
			# try:
			# 	print('myMemory')
			# 	dest_text = MyMemoryTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
			# except:
			# 	pass
	if dest_text == '':
		if translator_to_use == 'pons':
			translator_to_use = 'google'
			try:				
				print('pons')
				dest_text = PonsTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
			except:
				pass
	return dest_text

def get_translation(src_text):
	dest_text = translate(src_text)
	print('get_translation',dest_text)
	if src_text == dest_text or dest_text == '':
		translation_attempt = 1
		while translation_attempt < 15:
			time.sleep(translation_attempt)
			dest_text = translate(src_text)
			if src_text == dest_text or dest_text == '':
				translation_attempt += translation_attempt
			else:
				translation_attempt = 16
	if dest_text != '' and src_text != dest_text:	
		add_translation_to_local_dictionary(src_text, dest_text)
	return dest_text

file = open( "source.txt", "r")
lines = file.readlines()
file.close()


outputlines = []
outputlines.append(lines[0])
outputlines.append(lines[1])
for linenumber in range (2,len(lines)):
	if ' - ' in lines[linenumber]:
		split_line = lines[linenumber].split(' - ')
		outputlines.append('')
		tr_word = split_line[0]
		en_word = split_line[1]
		es_translation = get_translation(tr_word)
		if len(split_line) < 3:
			split_line.append('no hint')
		outputlines[linenumber] = es_translation + ' - ' + tr_word.rstrip() + ' - ' + en_word.rstrip() + ', ' + split_line[2].rstrip() +'\n'
		print('outputlines[linenumber]', outputlines[linenumber])


with open('new_source.txt', 'w') as f:
    for item in outputlines:
        f.write("%s" % item)
