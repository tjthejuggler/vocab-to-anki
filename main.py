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
import json
from pydub import AudioSegment
from difflib import SequenceMatcher
import sys, getopt
import random
import sqlite3
from operator import itemgetter
import zipfile
import argparse


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()
using_two_langs = False
first_lang = ''
second_lang = ''
third_lang = ''
should_make_anki_deck = False
should_make_anki_deck_audio_only = False
should_download = False
should_translate = False
should_randomize_order = False
require_individual_words_for_audio = True
is_formatted = False
should_make_audio_lesson = False
first_lang_min_number_of_words = 1 #this can be used to ignore any single word definitions so we dont have to redo them
number_of_languages_given = 0
number_of_languages_to_download = 0
api_calls = 0
max_api_calls = 10000
max_lines = 100000
list_of_not_downloaded_mp3s = []
list_of_downloaded_mp3s = []
list_of_already_had_mp3s = []
list_of_previously_failed_mp3s = []
only_get_anki_cards_being_worked_on = False
use_anki_file = False
deck_name = ''
lines = []
url = ''

parser = argparse.ArgumentParser()
parser.add_argument("language1", help="first language code (en = english)")
parser.add_argument("-2", "--language2", help="second language code (en = english)")
parser.add_argument("-3", "--language3", help="third language code (en = english)")
parser.add_argument("-d", "--download", type = int,
						help="should download pronunciations from forvo, \
						number of languages to download, max number of api calls")
parser.add_argument("-l", "--linesmax", type = int,
						help="maximum number of lines to be processed")
parser.add_argument("-x", "--maxapis", type = int,
						help="maximum number of api calls allowed")
parser.add_argument("-k", "--apkgsource", help="use apkg file as source, \
						name of apkg file to use")
parser.add_argument("-c", "--reducedapkg", action="store_true", help="reduce the number of words in the apkg")
parser.add_argument("-t", "--translate", action="store_true",help="translate words and output formatted list")
parser.add_argument("-m", "--makeankideck", action="store_true",help="make an anki deck from formatted list")
parser.add_argument("-ma", "--makeankideckaudio", action="store_true",help="make an anki deck from formatted \
					list that is audio only")
parser.add_argument("-a", "--audiolesson", action="store_true",help="make audio lesson from formatted list")
parser.add_argument("-r", "--randomorder", action="store_true",help="randomize the order of the words being processed")
parser.add_argument("-q", "--requireindivwords", action="store_true",help="only make an audio lesson entry if all \
						individual words have been downloaded")

args = parser.parse_args()
first_lang = args.language1
if args.language2:
	second_lang = args.language2
	number_of_languages_given = number_of_languages_given+1
if args.language3:
	second_lang = args.language3
	number_of_languages_given = number_of_languages_given+1
if args.download:
	print('should_download')
	should_download = True
	number_of_languages_to_download = args.download
if args.maxapis:
	max_api_calls = args.maxapis
	print('max_api_calls', max_api_calls)
if args.linesmax:
	max_lines = args.linesmax		
	print('max_lines', max_lines)
if args.apkgsource:
	use_anki_file = True
	deck_name = args.apkgsource		
	print('deck_name', deck_name)		
if args.translate:
	should_translate = True
if args.reducedapkg:
	only_get_anki_cards_being_worked_on = True	
if args.makeankideck:
	should_make_anki_deck = True
if args.makeankideckaudio:
	should_make_anki_deck = True
	should_make_anki_deck_audio_only = True
	print('should_make_anki_deck_audio_only', should_make_anki_deck_audio_only)
if args.audiolesson:
	should_make_audio_lesson = True
if args.requireindivwords:
	require_individual_words_for_audio = True	
if args.randomorder:
	should_randomize_order = True

if number_of_languages_to_download == '':
	number_of_languages_to_download = number_of_languages_given	
		
print('l1', first_lang)
print('21', second_lang)
print('3l', third_lang)
print('should_make_anki_deck',should_make_anki_deck)
print('should_download', should_download)
print('should_translate', should_translate)
print('number_of_languages_given', number_of_languages_given)
print('number_of_languages_to_download', number_of_languages_to_download)

new_deck_name = deck_name

if should_make_anki_deck_audio_only:
	new_deck_name = new_deck_name + 'only'



deck = genanki.Deck(round(time.time()), new_deck_name)

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

def get_word_list_from_apkg(filename, only_get_anki_cards_being_worked_on):
	with zipfile.ZipFile(filename+".apkg", 'r') as zip_ref:
		zip_ref.extractall(cwd+"/unzipped_apkg/"+filename)
	accepted_cards = []
	connection = sqlite3.connect(cwd+"/unzipped_apkg/"+filename+"/collection.anki2")  # connect to your DB
	cursor = connection.cursor()  # get a cursor
	cursor.execute("SELECT nid,ivl,due,factor FROM cards")  # execute a simple SQL select query
	card_selection = cursor.fetchall()  # get all the results from the above query
	for nid,ivl,due,factor in card_selection:
		cursor2 = connection.cursor()
		cursor2.execute("SELECT flds FROM notes WHERE id="+str(nid))
		flds_selection = cursor2.fetchall()
		fld = ' '.join(flds_selection[0])
		split_fld = fld.split('\x1f')
		word = re.sub("[\(\[].*?[\)\]]", "", split_fld[0]).strip()
		translation = split_fld[1]
		hint = split_fld[2]
		card_info = [word, translation, hint, ivl, factor]
		if only_get_anki_cards_being_worked_on:
			if ivl == 0 and due > 10000:
				accepted_cards.append(card_info)
			if ivl != 0 and ivl < 5:
				accepted_cards.append(card_info)			
				#print('word:',word,' translation:',translation,' ivl:',ivl,' due:',due,' factor:',factor)
		else:
			accepted_cards.append(card_info)
	#print(accepted_cards)
	accepted_cards = sorted(accepted_cards, key=itemgetter(2))
	print('--------------------')
	#print(accepted_cards)
	print('!!!!!!!')
	accepted_cards = accepted_cards[:max_lines]
	print(accepted_cards)
	lines_to_return = []
	for accepted_card in accepted_cards:
		new_card = accepted_card[0]+' - '+accepted_card[1]+' - '+accepted_card[2]
		if not new_card in lines_to_return:
			lines_to_return.append(new_card)
	return lines_to_return

def determine_if_formatted(lines):
	percent_formatted = 0
	formatted_line_count = 0
	is_formatted = True
	for line in lines:
		if ' - ' in line:
			formatted_line_count+=1
	if len(lines) != 0:	
		percent_formatted = formatted_line_count / len(lines)
	if percent_formatted < .9:
		is_formatted = False
	print('isformatted',is_formatted)
	return is_formatted

def create_anki_deck(my_deck, all_audio_files):
	my_package = genanki.Package(deck)
	my_package.media_files = all_audio_files
	my_package.write_to_file("anki/"+new_deck_name+'.apkg')

def create_anki_note(word, translation, hint, tag, url, all_audio_files):
	word_audio_file = word+'.mp3'
	each_audios = []
	for each in word:
		each_audios.append('[sound:'+each+'.mp3]')
	translation_audio_file = translation+'.mp3'
	if mp3_exists(word, first_lang):
		all_audio_files.append(pron_fold+'/'+first_lang+'/'+word_audio_file)
	if should_make_anki_deck_audio_only:
		if mp3_exists(translation, second_lang):
			all_audio_files.append(pron_fold+'/'+second_lang+'/'+translation_audio_file)
		my_note = genanki.Note(
						model=deck_model_audio_only,
						tags=[tag],
						fields=['[sound:'+word_audio_file+']' + ' ('+str(round(time.time()))+')', '[sound:'+translation_audio_file+']', word+'\n'+hint, url, word +' - '+translation])
	else:
		if using_two_langs:
			if mp3_exists(translation, second_lang):
				all_audio_files.append(pron_fold+'/'+second_lang+'/'+translation_audio_file)	
			my_note = genanki.Note(
				model=deck_model,
				tags=[tag],
				fields=[word + ' ('+str(round(time.time()))+')'+'[sound:'+word_audio_file+']', translation+'[sound:'+translation_audio_file+']', hint, url, ''])
		else:
			my_note = genanki.Note(
				model=deck_model,
				tags=[tag],
				fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+word_audio_file+']'])
				#fields=[word + ' ('+str(round(time.time()))+')', translation, hint, url, '[sound:'+word_audio_file+']'])

	#all_audio_files.append(cwd+'/'+second_lang+'/'+translation_audio_file)
	# my_note = genanki.Note(
	# 	model=deck_model,
	# 	tags=[tag],
	# 	fields=[word + ' ('+str(round(time.time()))+')'+'[sound:'+word_audio_file+']', translation+'[sound:'+translation_audio_file+']', hint, url, ])
	return my_note, all_audio_files

def has_previously_failed(word, lang):
	has_failed = False
	try:
		file = open(pron_fold+'/'+lang+'/'+lang+"_failed_words.txt", "r")
		lines = file.readlines()
		file.close()
		#print('has_previously_failed chec word',word)
		for line in lines:
			#print('has_previously_failed chec',line)
			if word.strip('\n') == line.strip('\n'):
				has_failed = True
	except:
		print(lang +' folder does not exist')
	return has_failed

def mp3_exists(translation, lang):
	exists = False
	try:
		with open(pron_fold+'/'+lang+'/'+translation+'.mp3') as f:
			exists = True
	except IOError:
		#print("File does not exist", translation)
		pass
	return exists

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
		my_json = json.dumps(local_dict)
		f = open(cwd+'/local_dictionaries/'+local_dict_file,"w")
		f.write(my_json)
		f.close()

def get_translation_from_local_library(src_text):
	local_dict_file = first_lang+'_'+second_lang+'.json'
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]

	return dest_text

def get_translation(src_text):
	dest_text = get_translation_from_local_library(src_text)
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
	# Text can also be a sequence of strings, in which case this method
	# will return a sequence of results for each text.
	result = translate_client.translate(text, target_language=target)
	# print(u"Text: {}".format(result["input"]))
	# print(u"Translation: {}".format(result["translatedText"]))
	# print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
	return(format(result["translatedText"]))

def download_if_needed(word, lang):
	global api_calls
	global list_of_already_had_mp3s
	global list_of_previously_failed_mp3s
	global list_of_downloaded_mp3s
	global list_of_not_downloaded_mp3s
	if api_calls < max_api_calls:
		if not has_previously_failed(word, lang):
			if not mp3_exists(word, lang):
				#print('did download',line)
				new_api_calls = DownloadMp3ForAnki(word, lang)
				api_calls = api_calls + new_api_calls
				if new_api_calls == 1:
					list_of_not_downloaded_mp3s.append(word)
				else:
					list_of_downloaded_mp3s.append(word)
			else:
				list_of_already_had_mp3s.append(word)
				print(' '*60,'MP3 already exists',word)
		else:
			list_of_previously_failed_mp3s.append(word)
			print(' '*40,'has previously failed',word)
	else:
		print('\nMax API calls reached!')
		program_end()

def show_translate_stats():
	print('\nTRANSLATE STATS')

def show_download_stats():
	print('\nDOWNLOAD STATS')
	print('API calls: ' + str(api_calls))
	print('successfully downloaded: '+str(len(list_of_downloaded_mp3s)))
	print('failed to download: '+str(len(list_of_not_downloaded_mp3s)))
	print('previously failed to download: '+str(len(list_of_previously_failed_mp3s)))
	print('already had: '+str(len(list_of_already_had_mp3s)))

def create_download_output_text():
	create_output_file('download_succeed', list_of_downloaded_mp3s)
	create_output_file('download_failed', list_of_not_downloaded_mp3s)
	create_output_file('download_previously', list_of_previously_failed_mp3s)
	create_output_file('download_already_have', list_of_already_had_mp3s)

def show_audio_lesson_stats(number_of_audio_lesson_passed):
	print('AUDIO LESSON STATS')
	print('entries passed: ', number_of_audio_lesson_passed)

def program_end():
	number_of_audio_lesson_passed = 0 #this needs dealt with
	print('\n')
	if should_translate:
		show_translate_stats()
	if should_download:
		show_download_stats()
		create_download_output_text()
	if should_make_audio_lesson:
		show_audio_lesson_stats(number_of_audio_lesson_passed)
	sys.exit()

def create_output_file(filename, output_lines):
	with open(cwd+'/output/'+filename + '.txt', 'w') as f:
		for item in output_lines:
			f.write("%s\n" % item)
#last word downloaded - yenilikler

def concatenate_words_into_mp3_if_needed(word_list, lang):
	if not mp3_exists(word_list, lang):
		mp3_to_export = []
		for word in word_list.split():
			print('conc word', word, lang)
			if mp3_exists(word, lang):
				print('making segment', word)
				mp3_to_export.append(remove_silence(AudioSegment.from_mp3(pron_fold+'/'+lang+'/'+word+'.mp3')))
		if mp3_to_export:
			cominedMP3 = sum(mp3_to_export)
			cominedMP3.export(pron_fold+'/'+lang+'/'+word_list+'.mp3', format="mp3")

def detect_leading_silence(sound, silence_threshold=-45.0, chunk_size=400):
    trim_ms = 0 # ms
    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size
    return trim_ms

def remove_silence(sound):
	start_trim = detect_leading_silence(sound)
	end_trim = detect_leading_silence(sound.reverse())
	duration = len(sound)    
	trimmed_sound = sound[start_trim:duration-end_trim]
	silence = AudioSegment.silent(duration=500)
	trimmed_sound_with_silence = trimmed_sound + silence
	return trimmed_sound

def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def add_apostrophe_if_needed(line):
	to_return = line
	file = line+'.mp3'
	local_dict_file = 'apos_previously_changed.json'
	if path.exists(cwd+'/scripts/'+local_dict_file):			
		with open(cwd+'/scripts/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if file in local_dict:
				to_return = local_dict[file].replace(".mp3","")
	#print(to_return, 'ret')
	return to_return

def clean_string(line):
	line = line.strip('\n')
	line = ' '.join(s for s in line.split() if not any(c.isdigit() for c in s)) #remove digits from string
	line = line.lower()
	return line

def remove_special_characters(line):
	return re.sub(r"[^\w\d'\s]",'',line)

def remove_special_characters_and_add_apostrophes(line):
	line = remove_special_characters(line)
	return add_apostrophe_if_needed(line)	

def split_and_download(word_to_download, lang):
	if len(word_to_download.split()) < 3:
		download_if_needed(word_to_download, lang)
		if not mp3_exists(word_to_download, lang) and len(word_to_download.split()) == 2:
			download_if_needed(word_to_download.split()[0], lang)
			download_if_needed(word_to_download.split()[1], lang)
	else:
		for word in word_to_download.split():
			download_if_needed(word, lang)

def get_hint_from_formatted_line(split_line):
	hint = ""
	if len(split_line) > 2:
		hint = split_line[2]
	return hint

def check_for_and_try_to_get_all_mp3s(first_word, first_lang, second_word, second_lang):
	have_all_mp3s = True
	for word in first_word.split():
		download_if_needed(word, first_lang)
		if require_individual_words_for_audio and not mp3_exists(word, first_lang):							
			have_all_mp3s = False
	for word in second_word.split():
		download_if_needed(word, second_lang)
		if require_individual_words_for_audio and not mp3_exists(word, second_lang):								
			have_all_mp3s = False
	if not mp3_exists(first_word, first_lang):
		have_all_mp3s = False										
	if not mp3_exists(second_word, second_lang):
		have_all_mp3s = False
	concatenate_words_into_mp3_if_needed(first_word, first_lang)
	concatenate_words_into_mp3_if_needed(second_word, second_lang)		
	return have_all_mp3s

def prepare_audio_lesson_item(first_word, first_lang, second_word, second_lang):
	audio = AudioSegment.silent(duration=10)
	text = ''
	print('making audio', first_word, second_word)
	first_sound = AudioSegment.from_mp3(pron_fold+'/'+second_lang+'/'+second_word+'.mp3')
	second_sound = AudioSegment.from_mp3(pron_fold+'/'+first_lang+'/'+first_word+'.mp3')
	long_silence = AudioSegment.silent(duration=second_sound.duration_seconds*2000)					
	short_silence = AudioSegment.silent(duration=second_sound.duration_seconds*1000)
	audio += first_sound + long_silence + second_sound + short_silence
	audio += second_sound + long_silence + second_sound + short_silence + second_sound
	text = first_word + ' - ' + second_word + ' - ' + hint
	return audio, text

def get_lines_from_source(deck_name, only_get_anki_cards_being_worked_on):
	if use_anki_file:
		print("deck_name", deck_name)
		lines = get_word_list_from_apkg(deck_name, only_get_anki_cards_being_worked_on)
		print('lines', lines)
	else:	
		file = open( "source.txt", "r")
		lines = file.readlines()
		file.close()
		deck_name = lines[0].replace(' ','_').strip()
		url = lines[1]
		lines = lines[2:]
	return lines

def main(deck_name, only_get_anki_cards_being_worked_on):
	lines = get_lines_from_source(deck_name, only_get_anki_cards_being_worked_on)
	is_formatted = determine_if_formatted(lines)
	if should_randomize_order == True:
		print("randomized lines")
		random.shuffle(lines)
	all_audio_files = []
	output_lines = []
	audio_text = []
	audio_lesson_output = AudioSegment.silent(duration=2000)
	audio_lesson_name = ''
	total_lines = 0
	for line in lines:
		print('line', line)
		total_lines+=1
		if total_lines == max_lines:
			break
		line = clean_string(line)
		if is_formatted == False :
			line = remove_special_characters(line)
			words = line.split()
			for word in words:
				word = add_apostrophe_if_needed(word)
				if should_translate:
					translation = get_translation(word).replace('-','/')
					if translation:
						output_lines.append(word + ' - ' + translation + ' - no hint\n')
				if should_download:
					download_if_needed(word, first_lang)
			if should_translate:
				create_output_file('new_source',output_lines)
		elif is_formatted == True:
			if should_make_anki_deck:
				tag = deck_name #this should actually be the first line with text
			if ' - ' in line:
				split_line = line.split(' - ')
				first_word = remove_special_characters_and_add_apostrophes(split_line[0])
				second_word = remove_special_characters_and_add_apostrophes(split_line[1])
				if should_download:
					split_and_download(first_word, first_lang)
					if number_of_languages_to_download > 1:
						split_and_download(second_word, second_lang)
				if should_translate:
					translation = get_translation(first_word).replace('-','/')
					if translation:
						output_lines.append(first_word + ' - ' + translation + ' - no hint')
					create_output_file('new_source',output_lines)
				hint = get_hint_from_formatted_line(split_line)
				if should_make_anki_deck:
					concatenate_words_into_mp3_if_needed(first_word, first_lang)
					note, all_audio_files = create_anki_note(first_word, second_word, hint, tag, url, all_audio_files)
					deck.add_note(note)
				if should_make_audio_lesson:
					have_all_mp3s = check_for_and_try_to_get_mp3s(first_word, first_lang, second_word, second_lang)
					if have_all_mp3s:
						audio, text = prepare_audio_lesson_item(first_word, first_lang, second_word, second_lang)
						audio_lesson_output += audio
						audio_text.append(text)
	rand_num = ''					
	if should_randomize_order:
		rand_num = str(random.randint(0, 100000))
	if should_make_audio_lesson:
		create_output_file(deck_name+rand_num+'_text', audio_text)								
	if should_make_audio_lesson:
		print('len(audio_lesson_output)',len(audio_lesson_output))
		audio_lesson_output.export(cwd+'/mp3_output/'+new_deck_name+rand_num+"_audio.mp3", format="mp3")
		print(deck_name+rand_num+"_audio.mp3 created")
	if should_make_anki_deck:
		create_anki_deck(deck, all_audio_files)
	program_end()

main(deck_name, only_get_anki_cards_being_worked_on)
