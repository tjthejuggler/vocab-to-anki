#this should make our ocal dictionaries print pretty and make everything in them lowercase
import json
import os
from os import path
import six
from google.cloud import translate_v2 as translate

target = 'en'

should_pretty_print = False
should_combine_opposite_dictionaries = False
should_combine_dictionaries = False
should_make_dictionary_lowercase = True
should_reorder_keys_and_values = False

cwd = os.getcwd()
local_dict = {}
local_dict_file = 'en_es.json'
if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
	with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
		local_dict = json.load(json_file)
print(len(local_dict))

def Merge(dict1, dict2):
    return(dict2.update(dict1))

def get_language(target, text):
    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["detectedSourceLanguage"]

def create_dict(dict_name, dictionary):
	my_json = json.dumps(dictionary)
	f = open(cwd+'/local_dictionaries/'+dict_name,"w")
	f.write(my_json)
	f.close()

if should_pretty_print:
	jsonString = local_dict
	print(jsonString)
	def get_pretty_print(json_object):
	    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))
	print(get_pretty_print(jsonString))
	my_json = get_pretty_print(jsonString)
	f = open(cwd+'/local_dictionaries/en_es_pretty.json',"w")
	f.write(my_json)
	f.close()

if should_combine_opposite_dictionaries:
	dict_to_merge = {}
	dict_to_merge_name = 'es_en.json'
	if path.exists(cwd+'/local_dictionaries/'+dict_to_merge_name):			
		with open(cwd+'/local_dictionaries/'+dict_to_merge_name) as json_file:
			dict_to_merge = json.load(json_file)
	print(dict_to_merge)
	print('\n'*10)
	swapped_dict = {y:x for x,y in dict_to_merge.items()}
	print(swapped_dict)
	print('\n'*10)
	Merge(swapped_dict, local_dict)
	print(local_dict)

	print(len(local_dict))

if should_combine_dictionaries:
	dict_to_merge = {}
	dict_to_merge_name = 'es_en.json'
	if path.exists(cwd+'/local_dictionaries/'+dict_to_merge_name):			
		with open(cwd+'/local_dictionaries/'+dict_to_merge_name) as json_file:
			dict_to_merge = json.load(json_file)
	print(len(dict_to_merge))
	print(len(local_dict))
	#local_dict = Merge(dict_to_merge, local_dict)
	local_dict.update(dict_to_merge)
	#print(local_dict)
	print(len(local_dict))
	create_dict(local_dict_file, local_dict)

if should_reorder_keys_and_values:
	reordered_dict = {}
	for key in local_dict:
		detected_lang = get_language(target, key)
		print('det', detected_lang)
		if detected_lang == 'es':
			print(' '*30+'swap', key, local_dict[key])
			reordered_dict[local_dict[key]] = key;
		else:
			print('dont swap', key, local_dict[key])
			reordered_dict[key] = local_dict[key]
		#print(reordered_dict)
	create_dict(local_dict_file, reordered_dict)

if should_make_dictionary_lowercase:
	lower_dict = dict((k.lower(), v.lower()) for k,v in local_dict.items())
	create_dict(local_dict_file, lower_dict)
