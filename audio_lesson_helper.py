from pydub import AudioSegment
import random
from pathlib import Path

home = str(Path.home())
pron_fold = home+'/pronunciations'

def create_normal_audio_lesson_entry(first_sound, second_sound, long_silence, short_silence):
	audio = AudioSegment.silent(duration=10)
	if second_sound.duration_seconds < 3:
		audio += first_sound + long_silence + second_sound + short_silence + second_sound + short_silence 
	else:
		audio += first_sound + long_silence + second_sound + short_silence
		audio += second_sound + long_silence + second_sound + short_silence + second_sound + short_silence 
	return audio

def create_reverse_audio_lesson_entry(first_sound, second_sound, long_silence, short_silence):
	audio = AudioSegment.silent(duration=10)
	if first_sound.duration_seconds < 3:
		audio += second_sound + long_silence + second_sound + short_silence + first_sound
		audio += short_silence + second_sound + short_silence 
	else:
		audio += second_sound + long_silence + second_sound + short_silence + first_sound
		audio += long_silence + second_sound + short_silence + second_sound + short_silence 
	return audio

def create_three_section_audio_lesson_entry(first_sound, second_sound, long_silence, short_silence, hint):
	audio = AudioSegment.silent(duration=10)
	one_sec_silence = AudioSegment.silent(duration=1000)
	spelling_silence = AudioSegment.silent(duration=first_sound.duration_seconds*1200)
	first_sounds_with_sil = second_sound + one_sec_silence + second_sound + one_sec_silence
	second_sounds_with_sil = first_sound + one_sec_silence + first_sound +one_sec_silence +first_sound + spelling_silence
	hints_with_sil = hint + one_sec_silence + hint + one_sec_silence
	audio += first_sounds_with_sil + second_sounds_with_sil + hints_with_sil
	return audio

def prepare_audio_lesson_item(first_word, first_lang, second_word, second_lang, hint, audio_text, audio_lesson_order_dict, three_part_audio_lesson):
	audio = AudioSegment.silent(duration=10)
	text = first_word + ' - ' + second_word + ' - ' + hint
	use_normal_order = True
	if text in audio_lesson_order_dict:
		use_normal_order = not audio_lesson_order_dict[text]
	else:
		random_bit = random.getrandbits(1)
		use_normal_order = bool(random_bit)
	print('making audio', first_word, second_word)
	first_sound = AudioSegment.from_mp3(pron_fold+'/'+second_lang+'/'+second_word+'_'+second_lang+'.mp3')
	second_sound = AudioSegment.from_mp3(pron_fold+'/'+first_lang+'/'+first_word+'_'+first_lang+'.mp3')
	long_silence = AudioSegment.silent(duration=second_sound.duration_seconds*2000)					
	short_silence = AudioSegment.silent(duration=second_sound.duration_seconds*1000)
	if three_part_audio_lesson:
		third_sound = AudioSegment.from_mp3(pron_fold+'/'+first_lang+'/'+hint.strip()+'_'+first_lang+'.mp3')
		audio = create_three_section_audio_lesson_entry(first_sound, second_sound, long_silence, short_silence, third_sound)
	else:
		if use_normal_order:
			audio = create_normal_audio_lesson_entry(first_sound, second_sound, long_silence, short_silence)
		else:
			audio = create_reverse_audio_lesson_entry(first_sound, second_sound, long_silence, short_silence)
	return audio, text, use_normal_order