import genanki
import time
import os
from os import path

#add andoird studio to path or figure out how to make an icon

file = open( "source.txt", "r")
lines = file.readlines()
file.close()

deckName = lines[0].replace(' ','_')

deck = genanki.Deck(round(time.time()), deckName)

deck_model = genanki.Model(
	1607393319,
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

def create_anki_note(word, translation, hint, tag, url):
	my_note = genanki.Note(
		model=deck_model,
		tags=[tag],
		fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url])
	return my_note

for line in lines:
	tag = lines[0].replace(' ','_') #this should actually be the first line with text
	url = lines[1]
	if ' - ' in line:
		split_line = line.split(' - ')
		word = split_line[0]
		translation = split_line[1]
		hint = ""
		if len(split_line) > 2:
			hint = split_line[2]
		note = create_anki_note(word, translation, hint, tag, url)
		deck.add_note(note)

genanki.Package(deck).write_to_file(deckName+'.apkg')
