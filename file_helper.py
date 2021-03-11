from pathlib import Path

home = str(Path.home())
pron_fold = home+'/pronunciations'

def mp3_exists(translation, lang):
	exists = False
	try:
		with open(pron_fold+'/'+lang+'/'+translation+'.mp3') as f:
			exists = True
	except IOError:
		pass
	return exists

#this hasn't been tested
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