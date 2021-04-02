import re
from translation_helper import *
from string_helper import *
from pronunciation_download_helper import *

def get_chunk_count(lines, is_formatted, max_lines, operation_type, first_lang, second_lang, number_of_languages_to_download):
	lines = lines[:min(max_lines, len(lines))]
	chunk_count = 0
	if is_formatted:
		lines = lines[2:]
		for line in lines:
			first_line = ''
			second_line = ''
			if ' - ' in line:
				first_line = clean_string(line.split(' - ')[0])
				second_line = clean_string(line.split(' - ')[1])
			if operation_type == 'translated':
				translation = get_translation_from_local_library(first_line, first_lang, second_lang)
				if not translation:
					chunk_count = chunk_count + 1
			if operation_type == 'downloaded':
				if not mp3_exists(first_line, first_lang):
					chunk_count = chunk_count + 1
			if number_of_languages_to_download == 2:
				if not mp3_exists(second_line, second_lang):
					chunk_count = chunk_count + 1
	elif not is_formatted:
		chunk_count = 0
		for line in lines:
			phrases = re.split('[?.,!:]',line)
			for phrase in phrases:
				phrase = remove_special_characters(phrase)
				phrase = clean_string(phrase)
				if operation_type == 'translated':
					translation = get_translation_from_local_library(phrase, first_lang, second_lang)
					if not translation:
						chunk_count = chunk_count + 1
				if operation_type == 'downloaded':
					if not mp3_exists(phrase, first_lang):
						chunk_count = chunk_count + 1				
	return chunk_count

def get_confirmation(lines, using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download,
		should_translate, should_randomize_order, is_formatted, should_make_audio_lesson,
		only_get_anki_cards_being_worked_on, use_anki_file, first_lang, second_lang, third_lang,
		require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
		number_of_languages_to_download, max_api_calls,	max_lines, deck_name, new_deck_name):
	if should_translate:
		operation_type  = 'translated'
	elif any([should_download, should_make_anki_deck, should_make_anki_deck_audio_only, should_make_audio_lesson]):
		operation_type  = 'downloaded'
	else:
		operation_type = 'processed'
	print('Deck name: ', new_deck_name)
	print('Gathering confirmation data...')
	print('Items to be '+operation_type+': ', get_chunk_count(lines, is_formatted, max_lines, operation_type, first_lang, second_lang, number_of_languages_to_download))
	print('Max API calls: ', max_api_calls)
	input("Press Enter to continue.")

def show_translate_stats():
	print('\nTRANSLATE STATS')

def show_download_stats(api_calls, mp3_download_lists):
	print('\nDOWNLOAD STATS')
	print('API calls: ' + str(api_calls))
	print('successfully downloaded: '+str(len(mp3_download_lists[0])))
	print('failed to download: '+str(len(mp3_download_lists[1])))
	print('already had: '+str(len(mp3_download_lists[2])))

def show_audio_lesson_stats(number_of_audio_lesson_passed):
	print('AUDIO LESSON STATS')
	print('entries passed: ', number_of_audio_lesson_passed)