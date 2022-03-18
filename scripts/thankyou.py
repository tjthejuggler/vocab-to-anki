# it takes a list of eng languages, and makes a deck that is
# language name(target lang) - thank you(tar) - hint(eng)

from os import path
import os
import genanki
from pathlib import Path
import time
import json
from google.cloud import translate_v2 as translate
import six
from polyglot.text import Text
from polyglot.downloader import downloader
print(downloader.supported_languages_table("transliteration2"))
home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()[:-8]

file = open( "script_source.txt", "r")
lines = file.readlines()
file.close()

lang_pairs = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino', 'he': 'Hebrew'}


deck_model_audio_and_written = genanki.Model(
	163335419,
	'Simple Model With Hint',
	fields=[
		{'name': 'Question'},
		{'name': 'Answer'},
		{'name': 'Hint'},
	],
	templates=[
		{
			'name': 'Card 1',
			'qfmt': '{{Question}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
		},
		{
			'name': 'Card 2',
			'qfmt': '{{Answer}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Question}}',
		}
	])

def ty_create_anki_deck(deck, all_audio_files):
	my_package = genanki.Package(deck)
	my_package.media_files = all_audio_files
	my_package.write_to_file('thankyous.apkg')


pron_fold = home+'/pronunciations'

def mp3_exists(lang_trans, lang_code):
	exists = False
	try:
		with open(pron_fold+'/'+lang_code+'/'+lang_trans+'_'+lang_code+'.mp3') as f:
			exists = True
	except IOError:
		pass
	return exists

def ty_create_anki_note(lang_trans, thank_trans, lang_code, lang_full, all_audio_files):
	#print('tag', tag, word)
	lang_name_audio_file = lang_trans+'_'+lang_code+'.mp3'
	each_audios = []
	thankyou_audio_file = thank_trans+'_'+lang_code+'.mp3'
	if mp3_exists(lang_trans, lang_code):
		all_audio_files.append(pron_fold+'/'+lang_code+'/'+lang_name_audio_file)
	if mp3_exists(thank_trans, lang_code):
		all_audio_files.append(pron_fold+'/'+lang_code+'/'+thankyou_audio_file)
	this_fields = ['[sound:'+lang_name_audio_file+']' + ' ('+str(round(time.time()))+')', '[sound:'+thankyou_audio_file+']', lang_full]
	single_card = False
	my_note = genanki.Note(
						model=deck_model_audio_and_written,
						tags=[],
						fields=this_fields)
		
	return my_note, all_audio_files


def ty_get_lang_code(lang_full):
	lang_code_to_return = ''
	for lang_code, language_name in lang_pairs.items(): 
		#print('ty_language_name', language_name)
		#print('ty_lang_full', lang_full)
		if language_name == lang_full:
			#print('ty_lang_code', lang_code)
			lang_code_to_return = lang_code
	return lang_code_to_return

def ty_get_translation_from_local_library(word, lang_code):
	local_dict_file = 'en_'+lang_code+'.json'
	translation = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):	
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if word in local_dict:
				translation = local_dict[word]

	return translation

def translate_text(target, text):
	translate_client = translate.Client()
	if isinstance(text, six.binary_type):
		text = text.decode("utf-8")
	result = translate_client.translate(text, target_language=target)
	print(result)
	return(format(result["translatedText"]))


def main():
	all_audio_files = []
	deck = genanki.Deck(round(time.time()), "thankyous")

	for line in lines:
		
		lang_full = line.strip()
		lang_code = ty_get_lang_code(lang_full).strip()
		lang_trans = ty_get_translation_from_local_library(lang_full, lang_code).strip()
		thank_trans = ty_get_translation_from_local_library('thank you', lang_code).strip()
		if(lang_trans and thank_trans):

			print(lang_full, lang_code, lang_trans, thank_trans)

			blob = lang_trans
			text = Text(blob)
			print('lang_trans', lang_trans)
			for x in text.transliterate("en"):
				print('...', x)
			blob = thank_trans
			text = Text(blob)
			print('lang_trans', thank_trans)
			for x in text.transliterate("en"):
				print('...', x)
			#translate_text(lang_code, lang_full)


#todo
#TEST TRANSLITERATE WITH exact example from website
#if decide not to transliterate, then
#	get list of languages
#	run list through main program to translate and download

		note, all_audio_files = ty_create_anki_note(lang_trans, thank_trans, lang_code, lang_full, all_audio_files)
		deck.add_note(note)
		# output_lines.append(first_word + ' - ' + second_word + ' - ' + hint)
		# create_output_file(deck_name+'_output','output',output_lines)

	ty_create_anki_deck(deck, all_audio_files)

	with open('new_source.txt', 'w') as f:
		for item in lines:
			f.write("%s" % item)

main()