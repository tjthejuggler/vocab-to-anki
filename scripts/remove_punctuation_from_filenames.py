	import os
	from pathlib import Path
	from os import listdir
	from os.path import isfile, join
	import re
	#this is a script that renames all files in a directory to lowercase

	def contains_punc(name):
		return not bool(re.match('^[a-zA-Z0-9]*$',name))

	home = str(Path.home())
	pron_fold = home+'/projects/audio_lesson_extender'
	pron_fold = home+'/pronunciations'
	lang = 'tr'
	parent_dir = pron_fold+'/'+lang+'/'

	onlyfiles = [f for f in listdir(parent_dir) if isfile(join(parent_dir, f))]

	for file in onlyfiles:
		#if contains_punc(file) and 'mp3' in file:
		if '*' in file:
			print(file)
			os.rename(parent_dir+file, parent_dir+file.replace('*',''))
			#os.rename(parent_dir+file, parent_dir+re.sub(r'[^\w\s]','',file).replace('mp3','.mp3'))

	# with open( parent_dir, 'w') as fd:
	#     os.replace(old_name, new_name, src_dir_fd=fd)