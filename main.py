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
from definition_helper import *

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()

def get_args():
	using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_make_anki_deck_written_only, should_download = False, False, False, False, False
	should_translate, should_randomize_order, is_formatted, should_make_audio_lesson, three_part_audio_lesson = False, False, False, False, False
	only_get_anki_cards_being_worked_on, use_anki_file, should_skip_confirmation, use_forvo = False, False, False, True
	first_lang, second_lang, hint_lang, user_first_string, user_tags  = '', '', '', '', ''
	require_individual_words_for_audio, should_overwrite, indiv_source, show_anki_text = True, False, None, False
	remove_punctuation, user_super_system = True, ''
	first_lang_min_number_of_words = 1 #this can be used to ignore any single word definitions so we dont have to redo them
	number_of_languages_given, number_of_languages_to_download  = 0, 1
	max_api_calls = 10000
	max_lines = 100000
	alternate_pronunciations = 1
	deck_name = ''
	parser = argparse.ArgumentParser()
	parser.add_argument("language1", help="first language code (en = english)")
	parser.add_argument("-2", "--language2", help="second language code (en = english)")
	parser.add_argument("-d", "--download", type = int,
							help="should download pronunciations from forvo, \
							number of languages to download, max number of api calls")
	parser.add_argument("-l", "--linesmax", type = int,
							help="maximum number of lines to be processed")
	parser.add_argument("-x", "--maxapis", type = int,
							help="maximum number of api calls allowed")
	parser.add_argument("-k", "--apkgsource", help="use apkg file as source, \
							name of apkg file to use")
	parser.add_argument("-i", "--individualsource", help="use individual string as source, \
							give the phrase to be used here")
	parser.add_argument("-c", "--reducedapkg", action="store_true", help="reduce the number of words in the apkg")
	parser.add_argument("-t", "--translate", action="store_true",help="translate words and output formatted list")
	parser.add_argument("-m", "--makeankideck", action="store_true",help="make an anki deck from formatted list")
	parser.add_argument("-ma", "--makeankideckaudio", action="store_true",help="make an anki deck from formatted \
						list that is audio only")
	parser.add_argument("-maw", "--makeankideckwritten", action="store_true",help="make an anki deck from formatted \
						list that is written only")
	parser.add_argument("-a", "--audiolesson", action="store_true",help="make audio lesson from formatted list")
	parser.add_argument("-a3", "--audiolesson3", action="store_true",help="make three section audio lesson from formatted list")
	parser.add_argument("-r", "--randomorder", action="store_true",help="randomize the order of the words being processed")
	parser.add_argument("-q", "--requireindivwords", action="store_true",help="only make an audio lesson entry if all \
							individual words have been downloaded")
	parser.add_argument("-s", "--skipconfirmation", action="store_true",help="skip confirmation prompt")
	parser.add_argument("-hn", "--hinttranslation", help="language code to be used in hint translation")
	parser.add_argument("-p", "--alternatepronunciations", type = int, 
							help="the number of alternate pronuciations to download")
	parser.add_argument("-f", "--firststring", help="the first string in the source list that will be recognized")
	parser.add_argument("-g", "--addankitag", help="tag to be added to any anki deck")
	parser.add_argument("-v", "--noforvo", action="store_true", help="don't use forvo to download pronunciations")
	parser.add_argument("-o", "--overwritepronunciation", action="store_true", help="overwrite the pronunciation files \
							if they exist")
	parser.add_argument("-tx", "--showtext", action="store_true", help="show the text on each side of anki card")
	parser.add_argument("-pnc", "--leavepunctuation", action="store_true", help="do not remove punctuation")
	parser.add_argument("-ss", "--supersystem", help="tell it what you have, and what you want, \
							example: wen>wen-wtr_den")
	args = parser.parse_args()
	first_lang = args.language1
	if args.language2:
		second_lang = args.language2
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
	if args.individualsource:
		indiv_source = args.individualsource		
		print('indiv_source', indiv_source)				
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
	if args.makeankideckwritten:
		should_make_anki_deck = True
		should_make_anki_deck_written_only = True
		print('should_make_anki_deck_written_only', should_make_anki_deck_written_only)
	if args.audiolesson:
		should_make_audio_lesson = True
	if args.audiolesson3:
		should_make_audio_lesson = True
		three_part_audio_lesson = True
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
	if args.noforvo:
		use_forvo = False
	if args.overwritepronunciation:
		should_overwrite = True
	if args.showtext:
		show_anki_text = True
	if args.leavepunctuation:
		remove_punctuation = False
	if args.supersystem:
		user_super_system = args.supersystem
	return (using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_make_anki_deck_written_only, should_download,
			should_translate, should_randomize_order, should_skip_confirmation, is_formatted, should_make_audio_lesson, three_part_audio_lesson,
			only_get_anki_cards_being_worked_on, use_anki_file, indiv_source, first_lang, second_lang, hint_lang,
			require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
			number_of_languages_to_download, max_api_calls,	max_lines, deck_name, alternate_pronunciations, 
			user_first_string, user_tags, use_forvo, should_overwrite, show_anki_text, remove_punctuation, user_super_system)

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

def create_output_file(filename, foldername, output_lines):
	#print('creating output file', filename)
	with open(cwd+'/'+foldername+'/'+filename + '.txt', 'w') as f:
		for item in output_lines:
			f.write("%s\n" % item.strip("\n"))

def create_download_output_text(mp3_download_lists):
	create_output_file('download_succeed', 'output', mp3_download_lists[0])
	create_output_file('download_previously', 'output', mp3_download_lists[1])
	create_output_file('download_already_have', 'output', mp3_download_lists[2])

def format_matches_user_arg():
	return True

def result_of_super_system(line, user_super_system):
	original_word = line
	given_string = user_super_system.split("=")[0]
	#print('given_string', given_string)
	given_lang = given_string[1:]
	#print('given_lang', given_lang)
	what_we_want = user_super_system.split("=")[1]
	#print('what_we_want', what_we_want)
	string_to_return = ''
	for section in what_we_want.split("-"):
		#print('string_to_return1', string_to_return)
		for part in section.split("_"):
			#print('part', part)
			wanted_lang = part[1:]
			#print('wanted_lang', wanted_lang)
			if part.startswith('w'):
				if part == given_string:
					string_to_return += original_word.strip() + ' '
					#print('is same', original_word)
				else:				
					print('super')	
					translation = get_translation(original_word, given_lang, wanted_lang).replace('-','/') + ' '
					#print('is different', translation)
					string_to_return += translation
			if part.startswith('d'):
				definition = get_definition(original_word, wanted_lang)
				string_to_return += "["+definition+"]"
		string_to_return += ' - '
		#print('string_to_return2', string_to_return)

	string_to_return = string_to_return[:-3].replace('  - ', ' - ', 100)
	#print('string_to_return_final', string_to_return)
	return string_to_return
	
	
def main():
	(using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_make_anki_deck_written_only, should_download,
		should_translate, should_randomize_order, should_skip_confirmation, is_formatted, should_make_audio_lesson, three_part_audio_lesson,
		only_get_anki_cards_being_worked_on, use_anki_file, indiv_source, first_lang, second_lang, hint_lang,
		require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
		number_of_languages_to_download, max_api_calls,	max_lines, deck_name, alternate_pronunciations,
		user_first_string, user_tags, use_forvo, should_overwrite, show_anki_text, remove_punctuation, user_super_system) = get_args()
	api_calls, user_first_string_reached = 0, False
	list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_already_had_mp3s = [], [], []
	mp3_download_lists = [list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_already_had_mp3s]
	lines, new_deck_name, url = get_lines_from_source(deck_name, only_get_anki_cards_being_worked_on, use_anki_file, should_make_anki_deck_audio_only, max_lines)
	if indiv_source:
		lines = [indiv_source]
	deck = genanki.Deck(round(time.time()), new_deck_name)
	is_formatted = determine_if_formatted(lines)
	lines = remove_duplicate_lines(lines)
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
			only_get_anki_cards_being_worked_on, use_anki_file, first_lang, second_lang,
			require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
			number_of_languages_to_download, max_api_calls,	max_lines, deck_name, new_deck_name)
	create_output_file(new_deck_name, 'sources', lines)
	current_tag = 'unit1'
	if user_super_system:
		# given_instructions = user_super_system.split('=')[0]
		# if given_instructions.startswith('w') and not given_instructions.include('_') and not given_instructions.include('-'):
			
		if format_matches_user_arg():
			is_formatted = True
			print("using super system", user_super_system)
		else:
			print("Format doesn't match user input")
			exit()
	for line in lines:
		line = line.lower()
		api_limit_reached = False
		if should_make_audio_lesson and line == "beyond this point is just for audio lesson":
			stop_everything_except_make_audio = True
		total_lines+=1
		if total_lines == max_lines:
			break
		if user_super_system:
			#print('pre super line', line)
			line = result_of_super_system(line, user_super_system)
			#print('post super line', line)
		if is_formatted == False :
			if not line.startswith('unit'):
				line = clean_string(line)
			phrases = re.split('[?.,!:]',line)			
			for phrase in phrases:
				phrase = remove_special_characters(phrase)
				split_phrase = phrase.split()
				for word in split_phrase:
					phrase = phrase.replace(word, add_apostrophe_if_needed(word, first_lang))
				phrase = phrase.strip()
				if phrase == user_first_string or user_first_string == '':				
					user_first_string_reached = True
				if not user_first_string_reached: #TODO turn this into an opt?
					continue
				if phrase != "":
					if should_translate:
						print('should trans')
						if line.startswith('unit'):
							print('UNIT!!!!!!!!!!!!!!')
						translation = get_translation(phrase, first_lang, second_lang).replace('-','/')
						if translation:
							translation_hint = ''
							if not hint_lang == '':
								translation_hint = get_translation(phrase, first_lang, hint_lang).replace('-','/') + ', '
							output_lines.append(phrase + ' - ' + translation + ' - '+translation_hint+'no hint\n')
					if should_download:			
						#print(phrase)			
						if api_calls >= max_api_calls:  
							print('\nMax API calls reached!')
							program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)
						else:
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(phrase, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations, use_forvo, should_overwrite)
			if should_translate:
				create_output_file(deck_name+'_output', 'output',output_lines)
		elif is_formatted == True:
			if should_make_anki_deck:
				#print('inhere', line)
				if user_tags:
					tag = user_tags
				else:
					tag = deck_name #this should actually be the first line with text
				if line.startswith('unit'):
					#print('tagline', line)
					current_tag = line
				tag = current_tag
			if ' - ' in line:
				split_line = line.split(' - ')
				if should_make_anki_deck_written_only == False:
					first_word = convert_numbers_to_words(split_line[0], first_lang)
					if remove_punctuation:
						first_word = remove_special_characters_and_add_apostrophes(first_word, first_lang)
					second_word = convert_numbers_to_words(split_line[1], second_lang)
					if remove_punctuation:
						second_word = remove_special_characters_and_add_apostrophes(second_word, second_lang)
				else:
					first_word = split_line[0]
					second_word = split_line[1]
				hint = get_hint_from_formatted_line(split_line)
				if not hint_lang == '':
					hint = second_word
					#hint = hint.strip('\n')  + ', ' + get_translation(first_word, first_lang, hint_lang).replace('-','/')
				#print('hint', hint)
				if hint == '':
					hint = 'no hint'
				if first_word == user_first_string or user_first_string == '':				
					user_first_string_reached = True
				if not user_first_string_reached: #TODO turn this into an opt?
					continue
				if not stop_everything_except_make_audio:
					if should_download:
						#print('should_download')
						if api_calls >= max_api_calls:  
							print('\nMax API calls reached!')
							program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)
						else:						
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations, use_forvo, should_overwrite)
							if number_of_languages_to_download > 1:
								api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls, 1, use_forvo, should_overwrite)
					if should_translate:
						translation = get_translation(first_word, first_lang, second_lang).replace('-','/')
						if translation:
							output_lines.append(first_word + ' - ' + translation + ' - ' + hint)
						create_output_file(deck_name+'_output','output',output_lines)
					if should_make_anki_deck:
						#print('make deck2')
						only_first_word_audio = False
						if number_of_languages_to_download != 0 and should_make_anki_deck_written_only == False:
							#print('number_of_languages_to_download', number_of_languages_to_download)
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations, use_forvo, should_overwrite)
							if only_first_word_audio == False:
								api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls, 1, use_forvo, should_overwrite)
						if should_make_anki_deck_written_only == False:
							#print('make deck')
							for i in range(0, alternate_pronunciations):
								should_add = False
								if alternate_pronunciations == 1:
									should_add = True
								first_word_with_num = first_word
								if i > 0:
									should_add = True
									first_word_with_num = first_word+str(i)
									#print(first_word_with_num, "about to check")
									if not mp3_exists(first_word_with_num, first_lang):
										print(first_word_with_num, "doesnt exist")
										should_add = False
								if should_add:
									#print("added to anki deck", first_word_with_num)
									#print('newhint', hint)
									note, all_audio_files = create_anki_note(first_word_with_num, second_word, hint, tag, url, all_audio_files, first_lang, second_lang, should_make_anki_deck_audio_only, using_two_langs, show_anki_text, should_make_anki_deck_written_only, only_first_word_audio)
									deck.add_note(note)
									output_lines.append(first_word + ' - ' + second_word + ' - ' + hint)
									create_output_file(deck_name+'_output','output',output_lines)
						elif should_make_anki_deck_written_only:
							all_audio_files = []
							show_anki_text = True
							note, all_audio_files = create_anki_note(first_word, second_word, hint, tag, url, all_audio_files, first_lang, second_lang, should_make_anki_deck_audio_only, using_two_langs, show_anki_text, should_make_anki_deck_written_only)
							deck.add_note(note)
							output_lines.append(first_word + ' - ' + second_word + ' - ' + hint)
							create_output_file(deck_name+'_output','output',output_lines)
					output_lines2.append(first_word + ' - ' + second_word + ' - no hint')
					create_output_file(deck_name+'_everything','output',output_lines2)
				if should_make_audio_lesson:
					api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations, use_forvo, should_overwrite)
					api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls, 1, use_forvo, should_overwrite)
					if three_part_audio_lesson:
						api_limit_reached, api_calls, mp3_download_lists = download_if_needed(hint, first_lang, api_calls, mp3_download_lists, max_api_calls, 1, use_forvo, should_overwrite)
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
							audio, text, use_normal_order = prepare_audio_lesson_item(first_word_with_num, first_lang, second_word, second_lang, hint, audio_text, audio_lesson_order_dict, three_part_audio_lesson)
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
		create_output_file(deck_name+rand_num+'_text', 'output', audio_text)								
	if should_make_audio_lesson:
		print('len(audio_lesson_output)',len(audio_lesson_output))
		audio_lesson_output.export(cwd+'/mp3_output/'+new_deck_name+rand_num+"_audio.mp3", format="mp3")
		print(deck_name+rand_num+"_audio.mp3 created")
	if should_make_anki_deck:
		create_anki_deck(deck, new_deck_name, all_audio_files)
	program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)

main()
