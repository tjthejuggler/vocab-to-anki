import genanki
import time
import os
from os import path
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
from anki_helper import *
from file_helper import *
from audio_lesson_helper import *
from pronunciation_download_helper import *

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()

def get_args():
	using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download = False, False, False, False
	should_translate, should_randomize_order, is_formatted, should_make_audio_lesson = False, False, False, False
	only_get_anki_cards_being_worked_on, use_anki_file = False, False
	first_lang, second_lang, third_lang  = '', '', ''
	require_individual_words_for_audio = True
	first_lang_min_number_of_words = 1 #this can be used to ignore any single word definitions so we dont have to redo them
	number_of_languages_given, number_of_languages_to_download  = 0, 0
	max_api_calls = 10000
	max_lines = 100000	
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
	return (using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download,
			should_translate, should_randomize_order, is_formatted, should_make_audio_lesson,
			only_get_anki_cards_being_worked_on, use_anki_file, first_lang, second_lang, third_lang,
			require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
			number_of_languages_to_download, max_api_calls,	max_lines, deck_name)

def get_word_list_from_apkg(filename, only_get_anki_cards_being_worked_on, should_make_anki_deck_audio_only, max_lines):
	with zipfile.ZipFile(filename+".apkg", 'r') as zip_ref:
		zip_ref.extractall(cwd+"/unzipped_apkg/"+filename)
	new_deck_name = filename
	if should_make_anki_deck_audio_only:
		new_deck_name = new_deck_name + 'Only'
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
		print('split_fld', split_fld)
		word = ''
		translation = ''
		hint = ''
		using_audio_only_apkg = False
		if ' - ' in split_fld[4]:
			using_audio_only_apkg = True
		if using_audio_only_apkg:			
			word = split_fld[4].split(' - ')[0]
			translation = split_fld[4].split(' - ')[1]
			print('word',word)
			hint = 'no hint'
			if '\n' in split_fld[2]:
				hint = split_fld[2].split('\n')[1]
			elif '<br>' in split_fld[2]:
				hint = split_fld[2].split('<br>')[1]
			print('translation',translation)
			print('hint', hint)
		else:
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
	return lines_to_return, new_deck_name

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

def get_translation_from_local_library(src_text, first_lang, second_lang):
	local_dict_file = first_lang+'_'+second_lang+'.json'
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]

	return dest_text

def get_translation(src_text, first_lang, second_lang):
	dest_text = get_translation_from_local_library(src_text, first_lang, second_lang)
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
	result = translate_client.translate(text, target_language=target)
	return(format(result["translatedText"]))

def show_translate_stats():
	print('\nTRANSLATE STATS')

def show_download_stats(api_calls, mp3_download_lists):
	print('\nDOWNLOAD STATS')
	print('API calls: ' + str(api_calls))
	print('successfully downloaded: '+str(len(mp3_download_lists[0])))
	print('failed to download: '+str(len(mp3_download_lists[1])))
	print('previously failed to download: '+str(len(mp3_download_lists[2])))
	print('already had: '+str(len(mp3_download_lists[3])))

def create_download_output_text(mp3_download_lists):
	create_output_file('download_succeed', mp3_download_lists[0])
	create_output_file('download_failed', mp3_download_lists[1])
	create_output_file('download_previously', mp3_download_lists[2])
	create_output_file('download_already_have', mp3_download_lists[3])

def show_audio_lesson_stats(number_of_audio_lesson_passed):
	print('AUDIO LESSON STATS')
	print('entries passed: ', number_of_audio_lesson_passed)

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

def get_hint_from_formatted_line(split_line):
	hint = ""
	if len(split_line) > 2:
		hint = split_line[2]
	return hint

def get_lines_from_source(deck_name, only_get_anki_cards_being_worked_on, use_anki_file, should_make_anki_deck_audio_only, max_lines):
	lines = []
	url = ''
	if use_anki_file:
		print("deck_name", deck_name)
		lines, new_deck_name = get_word_list_from_apkg(deck_name, only_get_anki_cards_being_worked_on, should_make_anki_deck_audio_only, max_lines)
		print('lines', lines)
	else:	
		file = open( "source.txt", "r")
		lines = file.readlines()
		file.close()
		new_deck_name = lines[0].replace(' ','_').strip()
		url = lines[1]
		lines = lines[2:]
	return lines, new_deck_name, url

def get_confirmation():
	input("Press Enter to continue...")

def main():
	(using_two_langs, should_make_anki_deck, should_make_anki_deck_audio_only, should_download,
		should_translate, should_randomize_order, is_formatted, should_make_audio_lesson,
		only_get_anki_cards_being_worked_on, use_anki_file, first_lang, second_lang, third_lang,
		require_individual_words_for_audio, first_lang_min_number_of_words,	number_of_languages_given, 
		number_of_languages_to_download, max_api_calls,	max_lines, deck_name) = get_args()
	api_calls = 0
	list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_previously_failed_mp3s, list_of_already_had_mp3s = [], [], [], []
	mp3_download_lists = [list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_previously_failed_mp3s, list_of_already_had_mp3s]
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
	all_audio_files, output_lines, audio_text = [], [], []
	audio_lesson_output, audio_lesson_name = AudioSegment.silent(duration=2000), ''
	total_lines = 0
	get_confirmation()
	for line in lines:
		api_limit_reached = False
		if should_make_audio_lesson and line == "beyond this point is just for audio lesson":
			stop_everything_except_make_audio = True
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
					translation = get_translation(word, first_lang, second_lang).replace('-','/')
					if translation:
						output_lines.append(word + ' - ' + translation + ' - no hint\n')
				if should_download:
					if api_calls >= max_api_calls:  
						print('\nMax API calls reached!')
						program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)
					else:
						api_limit_reached, api_calls, mp3_download_lists = download_if_needed(word, first_lang, api_calls, mp3_download_lists, max_api_calls)
			if should_translate:
				create_output_file('new_source',output_lines)
		elif is_formatted == True:
			if should_make_anki_deck:
				tag = deck_name #this should actually be the first line with text
			if ' - ' in line:
				split_line = line.split(' - ')
				first_word = remove_special_characters_and_add_apostrophes(split_line[0])
				second_word = remove_special_characters_and_add_apostrophes(split_line[1])
				hint = get_hint_from_formatted_line(split_line)
				if not stop_everything_except_make_audio:
					if should_download:
						if api_calls >= max_api_calls:  
							print('\nMax API calls reached!')
							program_end(should_translate, should_download, should_make_audio_lesson, api_calls, mp3_download_lists)
						else:						
							api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls)
							if number_of_languages_to_download > 1:
								api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls)
					if should_translate:
						translation = get_translation(first_word, first_lang, second_lang).replace('-','/')
						if translation:
							output_lines.append(first_word + ' - ' + translation + ' - no hint')
						create_output_file('new_source',output_lines)
					if should_make_anki_deck:
						api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls)
						print(second_word)
						api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls)
						note, all_audio_files = create_anki_note(first_word, second_word, hint, tag, url, all_audio_files, first_lang, second_lang, should_make_anki_deck_audio_only, using_two_langs)
						deck.add_note(note)
				if should_make_audio_lesson:
					api_limit_reached, api_calls, mp3_download_lists = download_if_needed(first_word, first_lang, api_calls, mp3_download_lists, max_api_calls)
					api_limit_reached, api_calls, mp3_download_lists = download_if_needed(second_word, second_lang, api_calls, mp3_download_lists, max_api_calls)
					audio, text, use_normal_order = prepare_audio_lesson_item(first_word, first_lang, second_word, second_lang, hint, audio_text, audio_lesson_order_dict)
					audio_lesson_order_dict[text] = use_normal_order
					audio_lesson_output += audio
					audio_text.append(text)
		if api_limit_reached:
			Print('API limit reached.')
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
