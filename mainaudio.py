import genanki
import time
import os
from os import path
from frtest import DownloadMp3ForAnki
import re
from pathlib import Path
import sys
import six
from google.cloud import translate_v2 as translate

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

using_two_langs = False
first_lang = ''
second_lang = ''
third_lang = ''
should_make_cards = True
should_download = False
should_translate = False
already_formatted = True
first_lang_min_number_of_words = 1 #this can be used to ignore any single word definitions so we dont have to redo them
number_of_languages_given = 0
number_of_languages_to_download = 0
# if len(sys.argv) > 1:
# 	first_lang = sys.argv[1]
# else:
# 	print('you need at least one language')
# 	quit()

# if len(sys.argv) > 2:
# 	second_lang = sys.argv[2]
# 	using_two_langs = True

import sys, getopt

	# -l1 first language
	# -l2 second language
	# -l3 third language
	# -dl download
	# -dl1 only download first language
	# -tr translate
	# -mc make cards

#def main(argv):
inputfile = ''
outputfile = ''
try:
	opts, args = getopt.getopt(sys.argv[1:],"htm1:2:3:d:")
	print(opts)
except getopt.GetoptError:
	print ('test.py -i <inputfile> -o <outputfile>')
	sys.exit(2)
for opt, arg in opts:
	print(opt)
	if opt == '-h':
		print ('help')
		sys.exit()
	elif opt in ("-1"):
		print('1',arg)
		first_lang = arg
		number_of_languages_given = number_of_languages_given+1
	elif opt in ("-2"):
		second_lang = arg
		number_of_languages_given = number_of_languages_given+1
	elif opt in ("-3"):
		third_lang = arg
		number_of_languages_given = number_of_languages_given+1
	elif opt in ("-d"):
		should_download = True
		number_of_languages_to_download = arg
	elif opt in ("-t"):
		should_translate = True
	elif opt in ("-m"):
		should_make_cards = True
if number_of_languages_to_download == '':
	number_of_languages_to_download = number_of_languages_given				
print('l1', first_lang)
print('21', second_lang)
print('3l', third_lang)
print('should_make_cards',should_make_cards)
print('should_download', should_download)
print('should_translate', should_translate)
print('number_of_languages_given', number_of_languages_given)
print('number_of_languages_to_download', number_of_languages_to_download)

already_formatted = True

# if __name__ == "__main__":
#    main(sys.argv[1:])

print('1. Download only(first language - second language - third language)')
print('2. Translate only(first language -> second language: output.txt)')
print('3. Translate and download first language(first language -> second language: output.txt)')
print('4. Translate and download two languages(first language -> second language: output.txt)')
print('5. Translate, download, and make cards(output.txt)')
print('6. Download and make cards(word - translation - hint)')

while True:
	format_choice = input()
	if format_choice in ('1', '2', '3', '4', '5', '6'):
		break
	else:
		print('invalid choice')
		print('1. Download only(first language - second language - third language)')
		print('2. Translate only(first language -> second language: output.txt)')
		print('3. Translate and download first language(first language -> second language: output.txt)')
		print('4. Translate and download two languages(first language -> second language: output.txt)')
		print('5. Translate, download, and make cards(output.txt)')
		print('6. Download and make cards(word - translation - hint)')

print(format_choice)

format_choice = int(format_choice)

if format_choice > 4:
	should_make_cards = False

if format_choice != 2:
	should_download = True	

if format_choice != 1 and format_choice != 5:
	should_translate =  True

if format_choice == 6:
	already_formatted == True

if format_choice == 1:
	number_of_languages_to_download = len(sys.argv) - 1

if format_choice == 3:
	number_of_languages_to_download = 1

if format_choice > 3:
	number_of_languages_to_download = 2

home = str(Path.home())
cwd = os.getcwd()
#add andoird studio to path or figure out how to make an icon
file = open( "source.txt", "r")
lines = file.readlines()
file.close()

deckName = lines[0].replace(' ','_')

deck = genanki.Deck(round(time.time()), deckName)

deck_model = genanki.Model(
	163335419,
	'Simple Model With Hint',
	fields=[
		{'name': 'Question'},
		{'name': 'Answer'},
		{'name': 'Hint'},
		{'name': 'URL'},
	],
	templates=[
		{
			'name': 'Card 1',
			'qfmt': '{{Question}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><a href={{URL}}>video</a>',
		},
		{
			'name': 'Card 2',
			'qfmt': '{{Answer}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Question}}<br><a href={{URL}}>video</a>',
		}
	])

def create_anki_deck(my_deck, all_audio_files):
	my_package = genanki.Package(deck)
	my_package.media_files = all_audio_files
	my_package.write_to_file(deckName+'.apkg')

def create_anki_note(word, translation, hint, tag, url, all_audio_files):	
	word_audio_file = word+'.mp3'
	translation_audio_file = translation+'.mp3'
	if mp3_exists(word, first_lang):
		all_audio_files.append(cwd+'/'+first_lang+'/'+word_audio_file)
	if using_two_langs:
		if mp3_exists(translation, second_lang):
			all_audio_files.append(cwd+'/'+second_lang+'/'+translation_audio_file)	
		my_note = genanki.Note(
			model=deck_model,
			tags=[tag],
			fields=[word + ' ('+str(round(time.time()))+')'+'[sound:'+word_audio_file+']', translation+'[sound:'+translation_audio_file+']', hint, url, ''])
	else:
		my_note = genanki.Note(
			model=deck_model,
			tags=[tag],
			fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+word_audio_file+']'])

	#all_audio_files.append(cwd+'/'+second_lang+'/'+translation_audio_file)
	my_note = genanki.Note(
		model=deck_model,
		tags=[tag],
		fields=[word + ' ('+str(round(time.time()))+')'+'[sound:'+word_audio_file+']', translation+'[sound:'+translation_audio_file+']', hint, url, ])
	return my_note, all_audio_files

def has_previously_failed(word, lang):
	file = open(cwd+'/'+lang+'/'+lang+"_failed_words.txt", "r")
	lines = file.readlines()
	file.close()
	has_failed = False
	#print('has_previously_failed chec word',word)
	for line in lines:
		#print('has_previously_failed chec',line)
		if word.strip('\n') == line.strip('\n'):
			has_failed = True
	return has_failed

def mp3_exists(translation, lang):
	exists = False
	try:
		with open(cwd+'/'+lang+'/'+translation+'.mp3') as f:
			exists = True
	except IOError:
		print("File does not exist", translation)
	return exists

def add_translation_to_local_dictionary(src_text, dest_text):
	print('add_translation_to_local_dictionary', dest_text)
	cwd = os.getcwd()
	local_dict_file = dest_langcode+'_'+src_langcode+'.json'
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

def get_translation_from_local_library(src_text):
	cwd = os.getcwd()
	local_dict_file = dest_langcode+'_'+src_langcode+'.json'
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]
				print('local dict used', dest_text)

	return dest_text

def get_translation(src_text):
	dest_text = get_translation_from_local_library(src_text)
	if dest_text == '':
		dest_text = translate_text(dest_langcode, src_text)
	else:
		print('got from local dict', src_text, dest_text)
	if dest_text == '':	
		translation_attempt = 1
		while translation_attempt < 15:
			time.sleep(translation_attempt)
			dest_text = translate_text(dest_langcode, src_text)
			if src_text == dest_text or dest_text == '':
				translation_attempt += translation_attempt
			else:
				translation_attempt = 16
	if dest_text != '' and dest_text != "None":
		add_translation_to_local_dictionary(src_text, dest_text)
	return dest_text

def translate_text(target, text):
	translate_client = translate.Client()
	if isinstance(text, six.binary_type):
		text = text.decode("utf-8")
	# Text can also be a sequence of strings, in which case this method
	# will return a sequence of results for each text.
	result = translate_client.translate(text, target_language=target)
	print(u"Text: {}".format(result["input"]))
	print(u"Translation: {}".format(result["translatedText"]))
	print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
	return(format(result["translatedText"]))


all_audio_files = []


for line in lines:
	line = line.strip('\n')
	line = re.sub(r'[^\w\s]','',line)
	line = ' '.join(s for s in line.split() if not any(c.isdigit() for c in s))
	if already_formatted == False:
		print(line)
		words = line.split()
		for word in words:
			if should_translate:
				print('should translate')
				#translate word and append(word - translation - no hint) to output_lines
					#we may also want a choice for append(word - translation - ENGLISH,no hint)
			if should_download:
				#do this for word and or translation(if required)
				if not has_previously_failed(word, first_lang):
					if not mp3_exists(word, first_lang):
						#print('did download',line)
						DownloadMp3ForAnki(word, first_lang)
					else:
						print('MP3 already exists',word)
				else:
					print('has previously failed',word)
			

			if should_make_cards:
				print('should make cards')

	else:
		if should_make_cards:
			tag = lines[0].replace(' ','_') #this should actually be the first line with text
			url = lines[1]		
		if ' - ' in line:
			split_line = line.split(' - ')		
			if len(word.split()) < 3:
				if not has_previously_failed(word, first_lang):
					if not mp3_exists(word, first_lang):
						#print('did download',word)
						DownloadMp3ForAnki(word, first_lang)
					else:
						print('MP3 already exists',word)
				else:
					print('has previously failed',word)
			translation = split_line[1]
			if using_two_langs:
				if len(translation.split()) < 3:
					if not has_previously_failed(translation, second_lang):
						if not mp3_exists(translation, second_lang):
							#print('did download',translation)
							DownloadMp3ForAnki(translation, second_lang)
						else:
							print('MP3 already exists',translation)
					else:
						print('has previously failed',translation)			
			hint = ""
			if len(split_line) > 2:
				hint = split_line[2]
			if should_make_cards:
				note, all_audio_files = create_anki_note(word, translation, hint, tag, url, all_audio_files)
				deck.add_note(note)


	


create_anki_deck(deck, all_audio_files)

#make a github for this