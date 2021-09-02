import sys
import re
import genanki
import time
from wordfreq import zipf_frequency
import requests
from requests.exceptions import HTTPError
if sys.platform == 'linux':
	import getch
else:
	import msvcrt
import wikipediaapi
# from nltk.stem.snowball import SnowballStemmer
# from nltk.stem import WordNetLemmatizer
import os
from epub_conversion.utils import open_book, convert_epub_to_lines
from os import path
#from langCodes import *
from pathlib import Path
import json

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()

article_deck = None
#lemmatizer = WordNetLemmatizer()
#stemmer = SnowballStemmer("english")
wiki_wiki = wikipediaapi.Wikipedia('en')

language_choices = ['spanish','english','turkish','afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi',  'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu', 'Filipino', 'Hebrew']

lang_pairs = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino', 'he': 'Hebrew'}

def get_lang_code(lang_submitted):
    lang_code_to_return = ''
    for lang_code, language_name in lang_pairs.items(): 
        if language_name == lang_submitted:
            lang_code_to_return = lang_code
    return lang_code_to_return

def get_lang_from_code(lang_code_submitted):
    lang_to_return = ''
    for lang_code, language_name in lang_pairs.items(): 
        if lang_code == lang_code_submitted:
            lang_to_return = language_name
    return lang_to_return

def get_google_definition(word_to_define):
	first_definition = ''
	try:
		response = requests.get('https://api.dictionaryapi.dev/api/v1/entries/en/'+word_to_define)
		response.raise_for_status()
		jsonResponse = response.json()
		values_view = jsonResponse[0]['meaning'].values()
		value_iterator = iter(values_view)
		first_value = next(value_iterator)
		values_view = first_value[0].values()
		value_iterator = iter(values_view)
		first_definition = next(value_iterator)
	except HTTPError as http_err:
	    pass
	except Exception as err:
	    pass
	return (first_definition)

def get_wikipedia_summary(word_to_define):
	to_return = ''
	page = wiki_wiki.page(word_to_define)
	if page.exists():
		to_return = page.summary.partition('.')[0] + '.'
	return to_return

def get_definition_from_web(word, lang):
	#global stemmer
	global wiki_wiki
	#stemmer = SnowballStemmer(get_lang_from_code(lang))
	wiki_wiki = wikipediaapi.Wikipedia(lang)
	word_forms = []
	word_forms.append(word)
	# word_forms.append(stemmer.stem(word))
	# word_forms.append(lemmatizer.lemmatize(word))
	# if word_forms[0] and word_forms[0][-1] == 's':
	# 	word_forms.append(word_forms[0][:-1])	
	# if word_forms[1] and word_forms[1][-1] == 't' or word_forms[1][-1] == 's':
	# 	word_forms.append(word_forms[1]+'ion')
	word_forms = list(dict.fromkeys(word_forms)) #remove duplicates from list
	definitions = []
	for word_form in word_forms:
		if word_form:
			wiki_def = get_wikipedia_summary(word_form).lower().replace('\n', ' ')
			if ' is ' in wiki_def:
				wiki_def = wiki_def.split('is ',1)[1].capitalize()
			if wiki_def and 'may refer to:' not in wiki_def:
				#definitions.append([wiki_def,word_form])
				definitions.append(wiki_def)
			google_def = get_google_definition(word_form)
			if google_def:
				#definitions.append([google_def,word_form])
				definitions.append(google_def)
	print('defs', definitions)
	comma_seperated_definitions = ','.join(str(v) for v in definitions)
	return comma_seperated_definitions

def get_definition(original_word, wanted_lang):
	definition = get_definition_from_local_library(original_word, wanted_lang)
	if definition == '':
		definition = get_definition_from_web(original_word, wanted_lang)
		print('got from web', original_word, definition)
	else:
		print(' '*20+'got from local dictionary', original_word, definition)
		#this is weird because it was copied from translation_helper
	#UNCOMMENTTHIS IF NOT USING GOOGLE CLOUD TRANSLATE
	# if definition == '':	
	# 	definition_attempt = 1
	# 	while definition_attempt < 15:
	# 		time.sleep(definition_attempt)
	# 		definition = translate_text(second_lang, original_word)
	# 		if original_word == definition or definition == '':
	# 			definition_attempt += definition_attempt
	# 		else:
	# 			definition_attempt = 16
	if definition != '' and definition != "None":
		add_definition_to_local_dictionary(original_word, wanted_lang, definition)
	return definition



def add_definition_to_local_dictionary(original_word, wanted_lang, definition):
	local_dict_file = wanted_lang+'_dict.json'
	local_dict = {}
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
	first_text = original_word
	second_text = definition
	if not first_text in local_dict:
		local_dict[first_text] = second_text
		my_json = json.dumps(local_dict, ensure_ascii=False, indent=1, sort_keys=True)
		f = open(cwd+'/local_dictionaries/'+local_dict_file,"w")
		f.write(my_json)
		f.close()

def get_definition_from_local_library(original_word, wanted_lang):
	local_dict_file = wanted_lang+'_dict.json'
	definition = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if original_word in local_dict:
				definition = local_dict[original_word]

	return definition



# def get_local_dictionary(first_lang, second_lang):
# 	langs = [first_lang, second_lang]
# 	aplhabetized_langs = langs.sort()
# 	swapped = True
# 	if langs == aplhabetized_langs:
# 		swapped = False
# 	local_dict_file = langs[0]+'_'+langs[1]+'.json'
# 	return local_dict_file, swapped