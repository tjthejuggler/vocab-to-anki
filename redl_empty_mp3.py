import os
from pathlib import Path
from os import listdir
from os.path import isfile, join
import re
from pronunciation_download_helper import *
#this is a script that renames all files in a directory to lowercase

def contains_punc(name):
	return not bool(re.match('^[a-zA-Z0-9]*$',name))

home = str(Path.home())
pron_fold = home+'/projects/audio_lesson_extender'
pron_fold = home+'/pronunciations'
#lang = 'tr'
#parent_dir = pron_fold+'/'+lang+'/'

langs = [name for name in os.listdir(pron_fold)]

for lang in langs:
	parent_dir = pron_fold+'/'+lang+'/'
	onlyfiles = [f for f in listdir(parent_dir) if isfile(join(parent_dir, f))]
	for file in onlyfiles:
		if '.mp3' in file and os.path.getsize(parent_dir+file) <= 1000:
			try:
				print('try')
				os.remove(parent_dir+file)
				print('removed', parent_dir+file)
			except OSError as e: # name the Exception `e`
				print("Failed with:", e.strerror) # look what it says
				print("Error code:", e.code)			
			word = file.replace('_'+lang+'.mp3', '')
			DownloadMp3ForAnki(word, lang, 1)
			print(file)
		#os.rename(parent_dir+file, parent_dir+re.sub(r'[^\w\s]','',file).replace('mp3','.mp3'))

# with open( parent_dir, 'w') as fd:
#     os.replace(old_name, new_name, src_dir_fd=fd)