import genanki
import time
import os
from os import path
from frtest import DownloadMp3ForAnki
import re
from pathlib import Path

print('Format')
print('1. es - tr - en, hint')
print('2. tr - en - hint')
<<<<<<< HEAD
print('3. tr - en - hint (Download en)')
print('4. en - tr - hint (Download en)')
format_choice = input()
print(format_choice)
using_two_langs = False
first_lang = 'es'
second_lang = 'tr'
if format_choice  == '1' or format_choice  == '3':
	using_two_langs = True
else:
	first_lang = 'tr'

if format_choice  == '2' or format_choice  == '3':	
	first_lang = 'tr'
	second_lang = 'en'

if format_choice  == '4':	
	first_lang = 'en'
	second_lang = 'tr'
home = str(Path.home())
cwd = os.getcwd()
#add andoird studio to path or figure out how to make an icon

=======
format_choice = input()
print(format_choice)
using_two_langs = False
if format_choice  == '1':
	using_two_langs = True

home = str(Path.home())
cwd = os.getcwd()
#add andoird studio to path or figure out how to make an icon
first_lang = 'es'
second_lang = 'tr'
>>>>>>> 176ab8e7bf9727cf3d9a669f44ef6a6740fedf7d
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
<<<<<<< HEAD
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

=======
			all_audio_files.append(cwd+'/'+second_lang+'/'+translation_audio_file)
	my_note = genanki.Note(
		model=deck_model,
		tags=[tag],
		fields=[word + ' ('+str(round(time.time()))+')'+'[sound:'+word_audio_file+']', translation+'[sound:'+translation_audio_file+']', hint, url, ])
>>>>>>> 176ab8e7bf9727cf3d9a669f44ef6a6740fedf7d
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

does_not_exist_counter = 0

def mp3_exists(translation, lang):
	exists = False
	try:
		with open(cwd+'/'+lang+'/'+translation+'.mp3') as f:
			exists = True
	except IOError:
		print("File does not exist", translation)
	return exists

all_audio_files = []
for line in lines:
	tag = lines[0].replace(' ','_') #this should actually be the first line with text
	url = lines[1]
	if ' - ' in line:
		split_line = line.split(' - ')
		word = split_line[0].strip('\n')
		word = re.sub(r'[^\w\s]','',word)
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
		note, all_audio_files = create_anki_note(word, translation, hint, tag, url, all_audio_files)
		deck.add_note(note)

create_anki_deck(deck, all_audio_files)

#make a github for this