import os
from os import path
from pathlib import Path
import json
from google.cloud import translate_v2 as translate
import six

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()

def add_translation_to_local_dictionary(src_text, dest_text, src_lang, dest_lang):
	local_dict_file = src_lang+'_'+dest_lang+'.json'
	local_dict = {}
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
	first_text = src_text
	second_text = dest_text
	if not first_text in local_dict:
		local_dict[first_text] = second_text
		my_json = json.dumps(local_dict, ensure_ascii=False, indent=1, sort_keys=True)
		f = open(cwd+'/local_dictionaries/'+local_dict_file,"w")
		f.write(my_json)
		f.close()

def get_translation_from_local_library(src_text, first_lang, second_lang):
	local_dict_file = first_lang+'_'+second_lang+'.json'
	print(local_dict_file)
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]

	return dest_text

def get_translation(src_text, first_lang, second_lang):
	dest_text = get_translation_from_local_library(src_text, first_lang, second_lang)
	if dest_text == '':
		dest_text = translate_text(second_lang, src_text).lower()
		print('got from google', src_text, dest_text)
	else:
		print(' '*20+'got from local dict', src_text, dest_text)
	#UNCOMMENTTHIS IF NOT USING GOOGLE CLOUD TRANSLATE
	# if dest_text == '':	
	# 	translation_attempt = 1
	# 	while translation_attempt < 15:
	# 		time.sleep(translation_attempt)
	# 		dest_text = translate_text(second_lang, src_text)
	# 		if src_text == dest_text or dest_text == '':
	# 			translation_attempt += translation_attempt
	# 		else:
	# 			translation_attempt = 16
	if dest_text != '' and dest_text != "None":
		add_translation_to_local_dictionary(src_text, dest_text, first_lang, second_lang)
		add_translation_to_local_dictionary(dest_text, src_text, second_lang, first_lang)
	return dest_text

def get_local_dictionary(first_lang, second_lang):
	langs = [first_lang, second_lang]
	aplhabetized_langs = langs.sort()
	swapped = True
	if langs == aplhabetized_langs:
		swapped = False
	local_dict_file = langs[0]+'_'+langs[1]+'.json'
	return local_dict_file, swapped

def translate_text(target, text):
	translate_client = translate.Client()
	if isinstance(text, six.binary_type):
		text = text.decode("utf-8")
	result = translate_client.translate(text, target_language=target)
	return(format(result["translatedText"]))
