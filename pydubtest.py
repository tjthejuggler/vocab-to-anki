from pydub import AudioSegment
import os

cwd = os.getcwd()

def mp3_exists(translation, lang):
	exists = False
	try:
		with open(cwd+'/'+lang+'/'+translation+'.mp3') as f:
			exists = True
	except IOError:
		print("File does not exist", translation)
	return exists

def combineMP3s(*argv):
	lang = 'en'
	sounds = []
	combinedMP3filename = ''
	for arg in argv:
		if mp3_exists(arg, lang):
			sounds.append(AudioSegment.from_mp3(cwd+"/"+lang+"/"+arg+".mp3"))
			if combinedMP3filename == '':
				combinedMP3filename = arg
			else:
				combinedMP3filename = combinedMP3filename + '_' + arg

	
	cominedMP3 = sum(sounds)
	cominedMP3.export(cwd+"/"+lang+"/"+combinedMP3filename+".mp3", format="mp3")

combineMP3s('helpful', 'mother', 'helping')


