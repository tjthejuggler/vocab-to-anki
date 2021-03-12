from pathlib import Path
from pydub import AudioSegment
from pronunciation_download_helper import *

home = str(Path.home())
pron_fold = home+'/pronunciations'

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

def check_for_and_try_to_get_mp3s(first_word, first_lang, second_word, second_lang, require_individual_words_for_audio, api_calls, mp3_download_lists, max_api_calls):
	have_all_mp3s = True
	for word in first_word.split():
		api_calls, mp3_download_lists = download_if_needed(word, first_lang, api_calls, mp3_download_lists, max_api_calls)
		if require_individual_words_for_audio and not mp3_exists(word, first_lang):							
			have_all_mp3s = False
	for word in second_word.split():
		api_calls, mp3_download_lists = download_if_needed(word, second_lang, api_calls, mp3_download_lists, max_api_calls)
		if require_individual_words_for_audio and not mp3_exists(word, second_lang):								
			have_all_mp3s = False
	if not mp3_exists(first_word, first_lang):
		have_all_mp3s = False										
	if not mp3_exists(second_word, second_lang):
		have_all_mp3s = False
	concatenate_words_into_mp3_if_needed(first_word, first_lang)
	concatenate_words_into_mp3_if_needed(second_word, second_lang)		
	return have_all_mp3s, api_calls, mp3_download_lists			