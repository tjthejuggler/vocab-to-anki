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

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

using_two_langs = False
first_lang = ''
second_lang = ''
third_lang = ''
should_make_cards = False
should_download = False
should_translate = False
should_randomize_order = False
already_formatted = True
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
# if len(sys.argv) > 1:
# 	first_lang = sys.argv[1]
# else:
# 	print('you need at least one language')
# 	quit()

# if len(sys.argv) > 2:
# 	second_lang = sys.argv[2]
# 	using_two_langs = True



	# -l1 first language
	# -l2 second language
	# -l3 third language
	# -d download
	# -dl1 only download first language
	# -tr translate
	# -mc make cards

#def main(argv):
inputfile = ''
outputfile = ''
try:
	opts, args = getopt.getopt(sys.argv[1:],"htmar1:2:3:d:x:y:")
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
		print('should_download')
		should_download = True
		number_of_languages_to_download = arg
	elif opt in ("-x"):
		max_api_calls = int(arg)		
		print('max_api_calls', max_api_calls)
	elif opt in ("-y"):
		max_lines = int(arg)		
		print('max_lines', max_lines)		
	elif opt in ("-t"):
		should_translate = True
	elif opt in ("-m"):
		should_make_cards = True
	elif opt in ("-a"):
		should_make_audio_lesson = True
	elif opt in ("-r"):
		should_randomize_order = True
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

home = str(Path.home())
pron_fold = home+'/pronunciations'
cwd = os.getcwd()
file = open( "source.txt", "r")
lines = file.readlines()
file.close()

deck_name = lines[0].replace(' ','_')
url = lines[1]

lines = lines[2:]

if should_randomize_order == True:
	random.shuffle(lines)

deck = genanki.Deck(round(time.time()), deck_name)

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
	my_package.write_to_file(deck_name+'.apkg')

def create_anki_note(word, translation, hint, tag, url, all_audio_files):
	word_audio_file = word+'.mp3'
	each_audios = []
	for each in word:
		each_audios.append('[sound:'+each+'.mp3]')
	translation_audio_file = translation+'.mp3'
	if mp3_exists(word, first_lang):
		all_audio_files.append(pron_fold+'/'+first_lang+'/'+word_audio_file)
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
		#has_failed = False
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
	#print('add_translation_to_local_dictionary', dest_text)
	#local_dict_file, swapped = get_local_dictionary(second_lang,first_lang)
	local_dict_file = src_lang+'_'+dest_lang+'.json'
	local_dict = {}
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
	# if swapped:
	# 	first_text = dest_text
	# 	second_text = src_text
	# else:
	first_text = src_text
	second_text = dest_text
	if not first_text in local_dict:
		#print('!!!',first_text,second_text)
		local_dict[first_text] = second_text
		my_json = json.dumps(local_dict)
		f = open(cwd+'/local_dictionaries/'+local_dict_file,"w")
		f.write(my_json)
		f.close()

def get_translation_from_local_library(src_text):
	#local_dict_file, swapped = get_local_dictionary(second_lang,first_lang)
	local_dict_file = first_lang+'_'+second_lang+'.json'
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			#print(json_file)
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]

			# if swapped:
			# 	if src_text in local_dict:
			# 		dest_text = local_dict[src_text]
			# 		#print('local dict used', dest_text)				
			# else:
			# 	dest_text = list(local_dict.keys())[list(local_dict.values()).index(src_text)]


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

def program_end():
	print('\n')
	print('API calls: ' + str(api_calls))
	print('successfully downloaded: '+str(len(list_of_downloaded_mp3s)))
	print('failed to download: '+str(len(list_of_not_downloaded_mp3s)))
	print('previously failed to download: '+str(len(list_of_previously_failed_mp3s)))
	print('already had: '+str(len(list_of_already_had_mp3s)))
	create_output_file('download_succeed', list_of_downloaded_mp3s)
	create_output_file('download_failed', list_of_not_downloaded_mp3s)
	create_output_file('download_previously', list_of_previously_failed_mp3s)
	create_output_file('download_already_have', list_of_already_had_mp3s)	
	sys.exit()

def create_output_file(filename, output_lines):
	with open(filename + '.txt', 'w') as f:
		for item in output_lines:
			f.write("%s\n" % item)
#last word downloaded - yenilikler

def concatenate_words_into_mp3(word_list, lang):
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
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
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



all_audio_files = []
output_lines = []
audio_text = []
audio_lesson_output = AudioSegment.silent(duration=2000)
audio_lesson_name = ''
total_lines = 0
for line in lines:
	total_lines+=1
	print(total_lines)
	if total_lines == max_lines:
		break
	line = line.strip('\n')
	line = ' '.join(s for s in line.split() if not any(c.isdigit() for c in s))
	line = line.lower()
	if already_formatted == False :
		line = re.sub(r'[^\w\s]','',line)
		#print(line)
		words = line.split()
		for word in words:
			if should_translate:
				translation = get_translation(word).replace('-','/')
				print(translation)
				if translation:
					output_lines.append(word + ' - ' + translation + ' - no hint\n')
				#translate word and append(word - translation - no hint) to output_lines
					#we may also want a choice for append(word - translation - ENGLISH,no hint)
			if should_download:
				download_if_needed(word, first_lang)
		if should_translate:
			create_output_file('new_source',output_lines)
			

		# 	if should_make_cards:
		# 		print('should make cards')


	else:
		if should_make_cards:
			tag = deck_name #this should actually be the first line with text
		if ' - ' in line:
			split_line = line.split(' - ')
			first_word = split_line[0]
			first_word = re.sub(r'[^\w\s]','',first_word)
			second_word = split_line[1]
			second_word = re.sub(r'[^\w\s]','',second_word)
			if should_download:
				if len(first_word.split()) < 3:
					download_if_needed(first_word, first_lang)
					if not mp3_exists(first_word, first_lang) and len(first_word.split()) == 2:
						download_if_needed(first_word.split()[0], first_lang)
						download_if_needed(first_word.split()[1], first_lang)
						#concatenate_words_into_mp3(first_word, first_lang)
				else:
					for word in first_word.split():
						download_if_needed(word, first_lang)
					#concatenate_words_into_mp3(first_word, first_lang)
			if should_translate:
				translation = get_translation(first_word).replace('-','/')
				if translation:
					output_lines.append(first_word + ' - ' + translation + ' - no hint')
				#translate word and append(word - translation - no hint) to output_lines
					#we may also want a choice for append(word - translation - ENGLISH,no hint)
				create_output_file('new_source',output_lines)




			# 	if not has_previously_failed(word, first_lang):
			# 		if not mp3_exists(word, first_lang):
			# 			#print('did download',word)
			# 			DownloadMp3ForAnki(word, first_lang)
			# 	# 	else:
			# 	# 		print('MP3 already exists',word)
			# 	# else:
			# 	# 	print('has previously failed',word)
			# translation = split_line[1]
			# if using_two_langs:
			# 	if len(translation.split()) < 3:
			# 		if not has_previously_failed(translation, second_lang):
			# 			if not mp3_exists(translation, second_lang):
			# 				#print('did download',translation)
			# 				DownloadMp3ForAnki(translation, second_lang)
			# 		# 	else:
			# 		# 		print('MP3 already exists',translation)
			# 		# else:
			# 		# 	print('has previously failed',translation)			
			hint = ""
			if len(split_line) > 2:
				hint = split_line[2]
			if should_make_cards:
				if not mp3_exists(first_word, first_lang):
					concatenate_words_into_mp3(first_word, first_lang)
				note, all_audio_files = create_anki_note(first_word, second_word, hint, tag, url, all_audio_files)
				deck.add_note(note)
			if should_make_audio_lesson:
				if not mp3_exists(first_word, first_lang):
					concatenate_words_into_mp3(first_word, first_lang)
				if not mp3_exists(second_word, second_lang):
					print(second_word, second_lang)
					concatenate_words_into_mp3(second_word, second_lang)
				have_all_mp3s = True
				for word in first_word.split():
					if not mp3_exists(word, first_lang):
						have_all_mp3s = False
				for word in second_word.split():
					if not mp3_exists(word, second_lang):
						have_all_mp3s = False
				if not mp3_exists(first_word, first_lang):
					print(first_word, first_lang, "doesnt exist1")
					have_all_mp3s = False										
				if not mp3_exists(second_word, second_lang):
					print(second_word, second_lang, "doesnt exist2")
					have_all_mp3s = False
				if have_all_mp3s:
					print('making audio', first_word, second_word)
					first_sound = AudioSegment.from_mp3(pron_fold+'/'+second_lang+'/'+second_word+'.mp3')
					second_sound = AudioSegment.from_mp3(pron_fold+'/'+first_lang+'/'+first_word+'.mp3')
					long_silence = AudioSegment.silent(duration=second_sound.duration_seconds*2000)					
					short_silence = AudioSegment.silent(duration=second_sound.duration_seconds*1000)
					audio_lesson_output += first_sound + long_silence + second_sound + short_silence
					audio_lesson_output += second_sound + long_silence + second_sound + short_silence + second_sound
					audio_text.append(first_word + ' - ' + second_word + ' - ' + hint)

if should_make_audio_lesson:
	create_output_file(deck_name+'_text', audio_text)					
					
if should_make_audio_lesson:
	audio_lesson_output.export(deck_name+"_audio.mp3", format="mp3")

if should_make_cards:
	create_anki_deck(deck, all_audio_files)

program_end()
