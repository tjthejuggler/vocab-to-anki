import genanki
import time
import os
from os import path
import re
from pathlib import Path
import sys
import six
#from google.cloud import translate_v2 as translate
#import json
from pydub import AudioSegment
#from difflib import SequenceMatcher
import sys, getopt
import random
#import sqlite3
#from operator import itemgetter
#import zipfile
import argparse
from anki_helper import *
from file_helper import *
from audio_lesson_helper import *
from pronunciation_download_helper import *
from translation_helper import *
from string_helper import *
from print_helper import *
from source_helper import *

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()

def get_args():
	using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download = False, False, False, False
	should_translate, should_randomize_order, is_formatted, should_make_audio_lesson = False, False, False, False
	only_get_anki_cards_being_worked_on, use_anki_file, should_skip_confirmation = False, False, False
	first_lang, second_lang, third_lang, hint_lang, user_first_string, user_tags  = '', '', '', '', '', ''
	require_individual_words_for_audio = True
	first_lang_min_number_of_words = 1 #this can be used to ignore any single word definitions so we dont have to redo them
	number_of_languages_given, number_of_languages_to_download  = 0, 1
	max_api_calls = 10000
	max_lines = 100000
	alternate_pronunciations = 1
	deck_name = ''
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
	parser.add_argument("-s", "--skipconfirmation", action="store_true",help="skip confirmation prompt")
	parser.add_argument("-hn", "--hinttranslation", help="language code to be used in hint translation")
	parser.add_argument("-p", "--alternatepronunciations", type = int, 
							help="the number of alternate pronuciations to download")
	parser.add_argument("-f", "--firststring", help="the first string in the source list that will be recognized")
	parser.add_argument("-g", "--addankitag", help="tag to be added to any anki deck")
	args = parser.parse_args()
	first_lang = args.language1
	if args.language2:
		second_lang = args.language2
		number_of_languages_given = number_of_languages_given+1
	if args.language3:
		second_lang = args.language3
		number_of_languages_given = number_of_languages_given+1
	if args.hinttranslation:
		hint_lang = args.hinttranslation
	if args.download:
		#number_of_languages_to_download = 0
		print('should_download2', args.download)		
		number_of_languages_to_download = args.download
		if number_of_languages_to_download != 9:
			should_download = True
		else:
			number_of_languages_to_download = 0
	#number_of_languages_to_download = 0
	if args.maxapis:
		max_api_calls = args.maxapis
		#print('max_api_calls', max_api_calls)
	if args.linesmax:
		max_lines = args.linesmax		
		#print('max_lines', max_lines)
	if args.apkgsource:
		use_anki_file = True
		deck_name = args.apkgsource		
		#print('deck_name', deck_name)		
	if args.translate:
		should_translate = True
	if args.reducedapkg:
		only_get_anki_cards_being_worked_on = True	
	if args.makeankideck:
		should_make_anki_deck = True
	if args.makeankideckaudio:
		should_make_anki_deck = True
		should_make_anki_deck_audio_only = True
		#print('should_make_anki_deck_audio_only', should_make_anki_deck_audio_only)
	if args.audiolesson:
		should_make_audio_lesson = True
	if args.requireindivwords:
		require_individual_words_for_audio = True	
	if args.randomorder:
		should_randomize_order = True
	if args.skipconfirmation:
		should_skip_confirmation = True	
	if args.alternatepronunciations:
		alternate_pronunciations = args.alternatepronunciations
	if args.firststring:
		user_first_string = args.firststring
	if args.addankitag:
		user_tags = args.addankitag
	# if number_of_languages_to_download == '':
	# 	number_of_languages_to_download = number_of_languages_given	
	# print('l1', first_lang)
	# print('21', second_lang)
	# print('3l', third_lang)
	# print('should_make_anki_deck',should_make_anki_deck)
	# print('should_download', should_download)
	# print('should_translate', should_translate)
	# print('number_of_languages_given', number_of_languages_given)
	# print('number_of_languages_to_download', number_of_languages_to_download)		
	return (using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download,
			should_translate, should_randomize_order, should_skip_confirmation,is_formatted, should_make_audio_lesson,
			only_get_anki_cards_being_worked_on, use_anki_file, first_lang, second_lang, third_lang, hint_lang,
			require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
			number_of_languages_to_download, max_api_calls,	max_lines, deck_name, alternate_pronunciations, 
			user_first_string, user_tags)

def program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists):
	number_of_audio_lesson_passed = 0 #this needs dealt with
	print('\n')
	if should_translate:
		show_translate_stats()
	if should_download:
		show_download_stats(api_calls, mp3_download_lists)
		create_download_output_text(mp3_download_lists)
	if should_make_audio_lesson:
		show_audio_lesson_stats(number_of_audio_lesson_passed)
	sys.exit()

def create_output_file(filename, output_lines):
	with open(cwd+'/output/'+filename + '.txt', 'w') as f:
		for item in output_lines:
			f.write("%s\n" % item.strip("\n"))

def create_download_output_text(mp3_download_lists):
	create_output_file('download_succeed', mp3_download_lists[0])
	create_output_file('download_previously', mp3_download_lists[1])
	create_output_file('download_already_have', mp3_download_lists[2])


def main():
	(using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download,
		should_translate, should_randomize_order, should_skip_confirmation, is_formatted, should_make_audio_lesson,
		only_get_anki_cards_being_worked_on, use_anki_file, first_lang, second_lang, third_lang, hint_lang,
		require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
		number_of_languages_to_download, max_api_calls,	max_lines, deck_name, alternate_pronunciations,
		user_first_string, user_tags) = get_args()
	api_calls, user_first_string_reached = 0, False
	list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_already_had_mp3s = [], [], []
	mp3_download_lists = [list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_already_had_mp3s]
	lines, new_deck_name, url = get_lines_from_source(deck_name, only_get_anki_cards_being_worked_on, use_anki_file, should_make_anki_deck_audio_only, max_lines)
	deck = genanki.Deck(round(time.time()), new_deck_name)
	is_formatted = determine_if_formatted(lines)
	stop_everything_except_make_audio = False
	audio_lesson_order_dict = {}
	if should_make_audio_lesson:
		original_lines = list(lines)
		print('beyond...')
		lines.append("beyond this point is just for audio lesson")
		for original_line in original_lines:
			lines.append(original_line)
	if should_randomize_order == True:
		print("randomized lines")
		random.shuffle(lines)
	all_audio_files, output_lines, audio_text, output_lines2 = [], [], [], []
	audio_lesson_output, audio_lesson_name = AudioSegment.silent(duration=2000), ''
	total_lines = 0
	if not should_skip_confirmation:
		get_confirmation(lines, using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download,
			should_translate, should_randomize_order, is_formatted, should_make_audio_lesson,
			only_get_anki_cards_being_worked_on, use_anki_file, first_lang, second_lang, third_lang,
			require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
			number_of_languages_to_download, max_api_calls,	max_lines, deck_name, new_deck_name)
	for line in lines:
		api_limit_reached = False
		if should_make_audio_lesson and line == "beyond this point is just for audio lesson":
			stop_everything_except_make_audio = True
		total_lines+=1
		if total_lines == max_lines:
			break
		if is_formatted == False :
			line = clean_string(line)
			phrases = re.split('[?.,!:]',line)			
			for phrase in phrases:
				phrase = remove_special_characters(phrase)
				split_phrase = phrase.split()
				for word in split_phrase:
					phrase = phrase.replace(word, add_apostrophe_if_needed(word, first_lang))
				if phrase != "":
					if should_translate:
						translation = get_translation(phrase, first_lang, second_lang).replace('-','/')
						if translation:
							translation_hint = ''
							if not hint_lang == '':
								translation_hint = get_translation(phrase, first_lang, hint_lang).replace('-','/') + ', '
							output_lines.append(phrase + ' - ' + translation + ' - '+translation_hint+'no hint\n')
					if should_download:						
						if api_calls >= max_api_calls:  
							print('\nMax API calls reached!')
							program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)
						else:
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(phrase, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations)
			if should_translate:
				create_output_file('new_source',output_lines)
		elif is_formatted == True:
			if should_make_anki_deck:
				if user_tags:
					tag = user_tags
				else:
					tag = deck_name #this should actually be the first line with text
			if ' - ' in line:
				split_line = line.split(' - ')
				first_word = convert_numbers_to_words(split_line[0], first_lang)
				first_word = remove_special_characters_and_add_apostrophes(first_word, first_lang)
				second_word = convert_numbers_to_words(split_line[1], second_lang)
				second_word = remove_special_characters_and_add_apostrophes(second_word, second_lang)
				hint = get_hint_from_formatted_line(split_line)
				print(first_word)
				if first_word == user_first_string or user_first_string == '':				
					user_first_string_reached = True
				if not user_first_string_reached: #TODO turn this into an opt?
					print('continue')
					continue
				if not stop_everything_except_make_audio:
					if should_download:
						print('should_download')
						if api_calls >= max_api_calls:  
							print('\nMax API calls reached!')
							program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)
						else:						
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations)
							if number_of_languages_to_download > 1:
								api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls, 1)
					if should_translate:
						translation = get_translation(first_word, first_lang, second_lang).replace('-','/')
						if translation:
							output_lines.append(first_word + ' - ' + translation + ' - no hint')
						create_output_file('new_source',output_lines)
					if should_make_anki_deck:
						if number_of_languages_to_download != 0:
							print('number_of_languages_to_download', number_of_languages_to_download)
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations)
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls, 1)
						for i in range(0, alternate_pronunciations):
							should_add = False
							if alternate_pronunciations == 1:
								should_add = True
							first_word_with_num = first_word
							if i > 0:
								should_add = True
								first_word_with_num = first_word+str(i)
								print(first_word_with_num, "about to check")
								if not mp3_exists(first_word_with_num, first_lang):
									print(first_word_with_num, "doesnt exist")
									should_add = False
							if should_add:
								print("added to anki deck", first_word_with_num)
								note, all_audio_files = create_anki_note(first_word_with_num, second_word, hint, tag, url, all_audio_files, first_lang, second_lang, should_make_anki_deck_audio_only, using_two_langs)
								deck.add_note(note)
								output_lines.append(first_word + ' - ' + second_word + ' - no hint')
								create_output_file('new_source',output_lines)
						output_lines2.append(first_word + ' - ' + second_word + ' - no hint')
						create_output_file('everything',output_lines2)
				if should_make_audio_lesson:
					api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations)
					api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls, 1)
					for i in range(0, alternate_pronunciations):
						if alternate_pronunciations == 1:
							should_add = True#something like this needs to go into makeaudio section below
						else:
							should_add = False
						first_word_with_num = first_word
						if i > 0:
							first_word_with_num = first_word+str(i)
							if not mp3_exists(first_word_with_num, first_lang):
								should_add = False
						if should_add:
							print("should add", first_word_with_num)
							audio, text, use_normal_order = prepare_audio_lesson_item(first_word_with_num, first_lang, second_word, second_lang, hint, audio_text, audio_lesson_order_dict)
							audio_lesson_order_dict[text] = use_normal_order
							audio_lesson_output += audio
							audio_text.append(text)
		if api_limit_reached:
			print('API limit reached.')
			program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)
			break
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
		create_anki_deck(deck, new_deck_name, all_audio_files)
	program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)

main()
