import os
from pathlib import Path
lang = 'nl'

home = str(Path.home())
pron_fold = home+'/projects/audio_lesson_extender'
pron_fold = home+'/pronunciations'
parent_dir = pron_fold+'/'+lang+'/'

def mp3_in_folder(translation):
	exists = False
	try:
		with open(pron_fold+'/'+lang+'/'+translation+'.mp3') as f:
			exists = True
	except IOError:
		pass
	return exists


file = open(pron_fold+'/'+lang+'/'+lang+"_failed_words.txt", "r")
lines = file.readlines()
file.close()
#print('has_previously_failed chec word',word)
for line in lines:
	line = line.strip('\n')
	if mp3_in_folder(line):
		os.remove(pron_fold+'/'+lang+'/'+line+".mp3")
		print(line)