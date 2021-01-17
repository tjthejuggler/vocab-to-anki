import genanki
import time
import os
from os import path
from frtest import DownloadMp3ForAnki

#add andoird studio to path or figure out how to make an icon
lang = 'tr'
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
		{'name': 'Audio'},
	],
	templates=[
		{
			'name': 'Card 1',
			'qfmt': '{{Question}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><a href={{URL}}>video</a>{{Audio}}',
		},
		{
			'name': 'Card 2',
			'qfmt': '{{Answer}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Question}}<br><a href={{URL}}>video</a>{{Audio}}',
		}
	])

def create_anki_deck(my_deck, all_audio_files):
	my_package = genanki.Package(deck)
	my_package.media_files = all_audio_files
	my_package.write_to_file(deckName+'.apkg')

def create_anki_note(word, translation, hint, tag, url, all_audio_files):
	audio_file = word+'.mp3'
	if mp3_exists(word):
		all_audio_files.append('/home/trillian/forvo/'+lang+'/'+audio_file)
	my_note = genanki.Note(
		model=deck_model,
		tags=[tag],
		fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+audio_file+']'])
	return my_note, all_audio_files

def mp3_exists(translation):
	exists = False
	try:
		with open('/home/trillian/forvo/'+lang+'/'+translation+'.mp3') as f:
			exists = True
	except IOError:
		print("File not accessible", translation)

	return exists

all_audio_files = []
for line in lines:
	tag = lines[0].replace(' ','_') #this should actually be the first line with text
	url = lines[1]
	if ' - ' in line:
		split_line = line.split(' - ')
		word = split_line[0]
		if len(word.split()) < 3:
			if not mp3_exists(word):
				print('did download',word)
				DownloadMp3ForAnki(word)
			else:
				print('did not download',word)
		translation = split_line[1]
		hint = ""
		if len(split_line) > 2:
			hint = split_line[2]
		note, all_audio_files = create_anki_note(word, translation, hint, tag, url, all_audio_files)
		deck.add_note(note)

create_anki_deck(deck, all_audio_files)

#make a github for this