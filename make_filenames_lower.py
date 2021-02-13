import os
from pathlib import Path
from os import listdir
from os.path import isfile, join

#this is a script that renames all files in a directory to lowercase

home = str(Path.home())
pron_fold = home+'/pronunciations'
lang = 'en'
parent_dir = pron_fold+'/'+lang+'/'

onlyfiles = [f for f in listdir(parent_dir) if isfile(join(parent_dir, f))]

for file in onlyfiles:
	if file != file.lower():
		print(file)
		os.rename(parent_dir+file, parent_dir+file.lower())

# with open( parent_dir, 'w') as fd:
#     os.replace(old_name, new_name, src_dir_fd=fd)