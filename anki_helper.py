import genanki
from file_helper import *
import time

deck_model_audio_and_written = genanki.Model(
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

deck_model_audio_only = genanki.Model(
	137694419,
	'Audio Only With Hint',
	fields=[
		{'name': 'Question'},
		{'name': 'Answer'},
		{'name': 'Hint'},
		{'name': 'URL'},		
		{'name': 'Words'},
	],
	templates=[
		{
			'name': 'Card 1',
			'qfmt': '{{Question}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}{{Words}}',
		},
		{
			'name': 'Card 2',
			'qfmt': '{{Answer}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Question}}{{Words}}',
		}
	])

deck_model_partial_back_pronunciation = genanki.Model(
	137694419,
	'Audio Only With Hint',
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

deck_model_written_only = genanki.Model(
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
			'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
		},
	])

deck_model_first_word_audio = genanki.Model(
	163333519,
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

deck_single_card_audio = genanki.Model(
	133694419,
	'Audio Only With Hint Single',
	fields=[
		{'name': 'Question'},
		{'name': 'Answer'},
		{'name': 'Hint'},
		{'name': 'URL'},		
		{'name': 'Words'},
	],
	templates=[
		{
			'name': 'Card 1',
			'qfmt': '{{Question}}{{#Hint}}<br>{{hint:Hint}}{{/Hint}}',
			'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}{{Words}}',
		},
	])

def create_anki_deck(deck, new_deck_name, all_audio_files):
	my_package = genanki.Package(deck)
	my_package.media_files = all_audio_files
	my_package.write_to_file("anki/"+new_deck_name+'.apkg')

def create_anki_note(word, translation, hint, tag, url, all_audio_files, first_lang, second_lang, should_make_anki_deck_audio_only, using_two_langs, show_anki_text, should_make_anki_deck_written_only, only_first_word_audio):
	#print('tag', tag, word)
	word_audio_file = word+'_'+first_lang+'.mp3'
	each_audios = []
	translation_audio_file = translation+'_'+second_lang+'.mp3'
	if mp3_exists(word, first_lang):
		all_audio_files.append(pron_fold+'/'+first_lang+'/'+word_audio_file)
	partial_back_pronunciation = False
	if should_make_anki_deck_audio_only and only_first_word_audio == False and partial_back_pronunciation == False:
		if mp3_exists(translation, second_lang):
			all_audio_files.append(pron_fold+'/'+second_lang+'/'+translation_audio_file)
		word_text = ''
		translation_text = ''
		if show_anki_text:
			word_text = word
			translation_text = translation
		this_fields = ['[sound:'+word_audio_file+']' + ' ('+str(round(time.time()))+')' + ' '+word_text, '[sound:'+translation_audio_file+']' + ' ' + translation_text, word+'\n'+hint, url, word +' - '+translation]
		single_card = False
		if single_card:
			my_note = genanki.Note(
							model=deck_single_card_audio,
							tags=[tag],
							fields=this_fields)
		else:
			my_note = genanki.Note(
							model=deck_model_audio_only,
							tags=[tag],
							fields=this_fields)			
	else:
		
		if partial_back_pronunciation:
			if mp3_exists(translation, second_lang):
				all_audio_files.append(pron_fold+'/'+second_lang+'/'+translation_audio_file)
			deck_model_to_use = deck_model_partial_back_pronunciation
			my_note = genanki.Note(
				model=deck_model_to_use,
				tags=[tag],
				fields=['[sound:'+word_audio_file+']' + ' '+ word +' ('+str(round(time.time()))+')', '[sound:'+translation_audio_file+']' + ' ' + translation + ' ' +hint, "no hint"])
				#fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+word_audio_file+']'])

		elif only_first_word_audio:
			deck_model_to_use = deck_model_first_word_audio
			my_note = genanki.Note(
				model=deck_model_to_use,
				tags=[tag],
				fields=['[sound:'+word_audio_file+']' + ' ('+str(round(time.time()))+')' + ' '+word, translation, word+'\n'+hint])
				#fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+word_audio_file+']'])
		else:	
			if should_make_anki_deck_written_only:
				deck_model_to_use = deck_model_written_only
			else:
				deck_model_to_use = deck_model_audio_and_written

			if using_two_langs:
				if mp3_exists(translation, second_lang):
					all_audio_files.append(pron_fold+'/'+second_lang+'/'+translation_audio_file)	
				my_note = genanki.Note(
					model=deck_model_to_use,
					tags=[tag],
					fields=[word + ' ('+str(round(time.time()))+')'+'[sound:'+word_audio_file+']', translation+'[sound:'+translation_audio_file+']', hint, url, ''])
			else:
				my_note = genanki.Note(
					model=deck_model_to_use,
					tags=[tag],
					fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+word_audio_file+']'])
					#fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+word_audio_file+']'])

	#all_audio_files.append(cwd+'/'+second_lang+'/'+translation_audio_file)
	# my_note = genanki.Note(
	# 	model=deck_model,
	# 	tags=[tag],
	# 	fields=[word + ' ('+str(round(time.time()))+')'+'[sound:'+word_audio_file+']', translation+'[sound:'+translation_audio_file+']', hint, url, ])
	return my_note, all_audio_files