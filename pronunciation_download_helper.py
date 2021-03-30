import requests
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import requests
import urllib
import urllib.parse
import json
from google.cloud import texttospeech
from synth_data_helper import *
#from file_helper import *

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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

def has_previously_failed(word, lang):
	has_failed = False
	try:
		file = open(pron_fold+'/'+lang+'/'+lang+"_failed_words.txt", "r")
		lines = file.readlines()
		file.close()
		#print('has_previously_failed chec word',word)
		for line in lines:
			#print('has_previously_failed chec',line)
			if word.strip('\n') == line.strip('\n'):
				has_failed = True
	except:
		print(lang +' failed list does not exist')
	return has_failed

def synthesize_text(text, lang):
	#print('lang', lang, text)
	"""Synthesizes speech from the input string of text."""
	lang_code, nm, sgen = get_synth_data(lang)
	if lang_code != '':
		client = texttospeech.TextToSpeechClient()
		input_text = texttospeech.SynthesisInput(text=text)
		# Note: the voice can also be specified by name.
		# Names of voices can be retrieved with client.list_voices().
		voice = texttospeech.VoiceSelectionParams(
		  language_code=lang_code,
		  name=nm,
		  ssml_gender=sgen,
		)
		audio_config = texttospeech.AudioConfig(
		  audio_encoding=texttospeech.AudioEncoding.MP3,
		  speaking_rate=0.8
		)
		response = client.synthesize_speech(
		  request={"input": input_text, "voice": voice, "audio_config": audio_config}
		)
		lang_dir = os.path.join(pron_fold,lang)
		file_name = text.replace('\n','')+'.mp3'
		file_path = os.path.join(lang_dir, file_name)
		with open(file_path, "wb") as out:
			out.write(response.audio_content)
			print(' '*9,':| MP3 Synthesized.', text, lang)
	else:
		print("No synth data for this language.")

def download_if_needed(word, lang, api_calls, mp3_download_lists, max_api_calls, alternate_pronunciations):
	api_limit_reached = False
	list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_already_had_mp3s = mp3_download_lists
	for i in range(0, alternate_pronunciations):
		word_with_num = word
		if i != 0:
			word_with_num = word + str(i)
		if not mp3_exists(word_with_num, lang):#instead of looping this stuff here, it should be looped in the actual download
			new_api_calls = DownloadMp3ForAnki(word, lang, alternate_pronunciations)
			api_calls = api_calls + new_api_calls
			if new_api_calls == 0:
				api_limit_reached = True
			elif new_api_calls == 1 and i == 0:
				synthesize_text(word, lang)
			list_of_downloaded_mp3s.append(word)
		else:
			list_of_already_had_mp3s.append(word)
			print(' '*60,'MP3 already exists',word)
	return api_limit_reached, api_calls, [list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, list_of_already_had_mp3s]

def ForvoRequest(QUERY, LANG, apikey, ACT='word-pronunciations', FORMAT='mp3', free= False):
	# action, default is 'word-pronunciations', query, language, apikey, TRUE if free api(default), FALSE if commercial
	# Return a list of link to mp3 pronunciations for the word QUERY in LANG language.
	# FORMAT='ogg' will return a list of link to ogg pronunciations 
	
	if free:#default
		base_url = 'http://apifree.forvo.com/'
	else:
		#TODO: add non free base url
		base_url = 'http://apicommercial.forvo.com/' #is it correct?
		
	query_u8 = QUERY

	
	key = [
		('action',ACT),
		('format','json'),
		('word',urllib.parse.quote(QUERY)),
		('language',LANG),
		('key',apikey)
		]
	
	url = base_url + '/'.join(['%s/%s' % a for a in key if a[1]]) + '/'
	
	#print(url)

	try:
		#r = requests.get(url)
		r = requests.get(url, headers=headers)

	except:
		print("api maxed out!!!!!!!!!")
		raise
		return None
	
	#data = r.json()
	#print(r.content.decode())
	data = json.loads(r.content.decode())
	if data == ['Limit/day reached.']:
		return 'apiMax'
	else:
		if data[u'items']:
			#we retrieved a non empty JSON.
			#the JSON is structured like this:
			#a dictionary with 2 items, their keys are:
			#-u'attributes' (linked to info about the request we made)
			#-u'items'      (linked to a list of dictionaries)
			#in the list there is a dictionary for every pronunciation, we will search for the "mp3path" key
			
			paths = []
			for i in data[u'items']:
				audioFormat = u'path'+FORMAT
				paths.append(i[audioFormat])
			return paths
			
		else:
			#The json hasn't a u'items' key
			return None

def fileChoose():
	#show a file choose dialog box
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	return filename
from pathlib import Path

def addToFailedList(word, lang):
	lines=''
	Path(pron_fold+'/'+lang).mkdir(parents=True, exist_ok=True)
	try:
		file = open(pron_fold+'/'+lang+'/'+lang+"_failed_words.txt", "r")
		lines = file.read()
		file.close()

	except:
		#print("file doesn't exist", word)
		pass
	lines = lines + ("\n"+word)
	text_file = open(pron_fold+'/'+lang+'/'+lang+"_failed_words.txt", "w")
	text_file.write(lines)
	text_file.close()

def DownloadMp3ForAnki(word, lang, alternate_pronunciations):
	api_call_count = 1
	with open('apikey.txt') as a:
	  APIKEY=a.read()
	lang_dir = os.path.join(pron_fold,lang)
	r = ForvoRequest(word,lang,APIKEY)
	if r:
		#TODO get the limit and put it here as a loop, if the limit is 0 then it means we are only getting one
		if r == "apiMax":
			api_call_count = 0
		else:
			api_call_count = 2
			#mp3 = requests.get(r[0])
			for i in range(0, alternate_pronunciations):
				word_with_num = word
				if i != 0:
					word_with_num = word + str(i)
				if not mp3_exists(word_with_num, lang):# gut the stuff that links it			   
					mp3 = requests.get(r[i], headers=headers)
					file_name   = word_with_num.replace('\n','')+'.mp3'
					file_path   = os.path.join(lang_dir, file_name)
						
					if not os.path.exists(lang_dir):
						os.makedirs(lang_dir)              
					else:
						with open(file_path,"wb") as out:
							#we open a new mp3 file and we name it after the word we're downloading.
							#The file it's opened in write-binary mode
							out.write(mp3.content)   
							print(':) MP3 created',word_with_num)
	else:                        
		#print(' '*20,':( not available from Forvo', word)
		addToFailedList(word, lang)

	return api_call_count

def DownloadMp3(urlList, limit, word, folder):
	#download a mp3 file, rename it and write it in a costum folder
	for i in range(0,limit):
		mp3 = requests.get(urlList[i])                 
		file_name   = word.replace('\n','')+'.{0}'.format(i)+'.mp3'
		file_path   = os.path.join(folder, file_name)
			
		if not os.path.exists(folder):
			os.makedirs(folder)              
		else:
			with open(file_path,"wb") as out:
				#we open a new mp3 file and we name it after the word we're downloading.
				#The file it's opened in write-binary mode
				out.write(mp3.content)
