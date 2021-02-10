import sys
import requests
import os
import urllib
import urllib.parse
from pathlib import Path
from gi.repository import Notify
import vlc
import time
<<<<<<< HEAD
import json


lang = 'en'
cwd = ''

def ForvoRequest(QUERY, LANG, ACT='word-pronunciations', FORMAT='mp3', free= False):
	apikey = '1aa4d6b055eabcb347cd91e99a2acf95'
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
	print(url)
	try:
		#r = requests.get(url)
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		r = requests.get(url, headers=headers)
	except:
		raise
		return None
	print(r.content.decode())
	#data = r.json()
	data = json.loads(r.content.decode())
	
	if data[u'items']:
		paths = []
		for i in data[u'items']:
			audioFormat = u'path'+FORMAT
			paths.append(i[audioFormat])
		print('paths\n\n\n\n\n\n\n', paths)
		return paths            
	else:
		print('None\n\n\n\n\n\n\n')
		return None

def fileChoose():
	#show a file choose dialog box
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	return filename

def addToFailedList(word):
	file = open(cwd+'/'+lang+'/'+lang+"_failed_words.txt", "r")
	lines = file.read()
	file.close()
	lines = lines + ("\n"+word)
	text_file = open(cwd+'/'+lang+'/'+lang+"_failed_words.txt", "w")
	text_file.write(lines)
	text_file.close()

def DownloadMp3(word):
	home        = cwd
	lang_dir    = os.path.join(home,lang)
	r = ForvoRequest(word,lang)
	if r:
		#download a mp3 file, rename it and write it in a costum folder
		#mp3 = requests.get(r[0])
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		mp3 = requests.get(r[0], headers=headers)                 
		file_name   = word.replace('\n','')+'.mp3'
		file_path   = os.path.join(lang_dir, file_name)
			
		if not os.path.exists(lang_dir):
			os.makedirs(lang_dir)              
		else:
			with open(file_path,"wb") as out:
				#we open a new mp3 file and we name it after the word we're downloading.
				#The file it's opened in write-binary mode
				out.write(mp3.content)   
				print('MP3 created',word)
				play_audio(word)
	else:      
		Notify.init("Forvo DL")
		Notify.Notification.new('not available from Forvo', word).show()                  
		addToFailedList(word)

def mp3_exists(translation):
	exists = False
	print(cwd)
	print(lang)
	print(translation)
	try:
		with open(lang+'/'+translation+'.mp3') as f:
=======


lang = 'tr'
cwd = 'projects/vocab-to-anki/'

def ForvoRequest(QUERY, LANG, ACT='word-pronunciations', FORMAT='mp3', free= True):
      apikey = '1aa4d6b055eabcb347cd91e99a2acf95'
      if free:#default
            base_url = 'http://apifree.forvo.com/'
      else:
            #TODO: add non free base url
            base_url = 'htttp://api.forvo.com/' #is it correct?            
      query_u8 = QUERY      
      key = [
            ('action',ACT),
            ('format','json'),
            ('word',urllib.parse.quote(QUERY)),
            ('language',LANG),
            ('key',apikey)
            ]
      
      url = base_url + '/'.join(['%s/%s' % a for a in key if a[1]]) + '/'
      
      try:
            r = requests.get(url)
      except:
            raise
            return None
      
      data = r.json()
      
      if data[u'items']:
            paths = []
            for i in data[u'items']:
                  audioFormat = u'path'+FORMAT
                  paths.append(i[audioFormat])
            return paths            
      else:
            return None

def fileChoose():
      #show a file choose dialog box
      Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
      filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
      return filename

def addToFailedList(word):
      file = open(cwd+'/'+lang+'/'+lang+"_failed_words.txt", "r")
      lines = file.read()
      file.close()
      lines = lines + ("\n"+word)
      text_file = open(cwd+'/'+lang+'/'+lang+"_failed_words.txt", "w")
      text_file.write(lines)
      text_file.close()

def DownloadMp3(word):
      home        = 'projects/vocab-to-anki'
      lang_dir    = os.path.join(home,lang)
      r = ForvoRequest(word,lang)
      if r:
            #download a mp3 file, rename it and write it in a costum folder
            mp3 = requests.get(r[0])                 
            file_name   = word.replace('\n','')+'.mp3'
            file_path   = os.path.join(lang_dir, file_name)
                  
            if not os.path.exists(lang_dir):
                  os.makedirs(lang_dir)              
            else:
                  with open(file_path,"wb") as out:
                        #we open a new mp3 file and we name it after the word we're downloading.
                        #The file it's opened in write-binary mode
                        out.write(mp3.content)   
                        print('MP3 created',word)
                        play_audio(word)
      else:      
            Notify.init("Forvo DL")
            Notify.Notification.new('not available from Forvo', word).show()                  
            addToFailedList(word)

def mp3_exists(translation):
	exists = False
	try:
		with open(cwd+'/'+lang+'/'+translation+'.mp3') as f:
>>>>>>> 176ab8e7bf9727cf3d9a669f44ef6a6740fedf7d
			exists = True
	except IOError:
		print("File does not exist", translation)
	return exists

def play_audio(word):
<<<<<<< HEAD

	p = vlc.MediaPlayer(lang+'/'+word+'.mp3')
=======
	p = vlc.MediaPlayer(cwd+'/'+lang+'/'+word+'.mp3')
>>>>>>> 176ab8e7bf9727cf3d9a669f44ef6a6740fedf7d
	p.play()
	time.sleep(10)

def Main():
	word = sys.argv[-1]
	print(word)
	if not mp3_exists(word):
<<<<<<< HEAD
		print('not exists')
		DownloadMp3(word)
	else:
		print('exists')
=======
		DownloadMp3(word)
	else:
>>>>>>> 176ab8e7bf9727cf3d9a669f44ef6a6740fedf7d
		play_audio(word)

Main()