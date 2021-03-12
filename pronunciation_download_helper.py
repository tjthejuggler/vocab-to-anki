import forvo
import requests
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import requests
import urllib
import urllib.parse
import json
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
            print(lang +' folder does not exist')
      return has_failed

def download_if_needed(word, lang, api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, max_api_calls):
      if api_calls < max_api_calls:
            if not has_previously_failed(word, lang):
                  if not mp3_exists(word, lang):
                        #print('did download',line)
                        new_api_calls = DownloadMp3ForAnki(word, lang)
                        api_calls = api_calls + new_api_calls
                        if new_api_calls == 1:
                              list_of_not_downloaded_mp3s.append(word)
                        else:
                              list_of_downloaded_mp3s.append(word)
                  else:
                        list_of_already_had_mp3s.append(word)
                        print(' '*60,'MP3 already exists',word)
            else:
                  list_of_previously_failed_mp3s.append(word)
                  print(' '*40,'has previously failed',word)
      else:
            print('\nMax API calls reached!')
            program_end()
      return api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s


def split_and_download(word_to_download, lang, api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, max_api_calls):
      if len(word_to_download.split()) < 3:
            api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s = download_if_needed(word_to_download, lang, api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, max_api_calls)
            if not mp3_exists(word_to_download, lang) and len(word_to_download.split()) == 2:
                  api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s = download_if_needed(word_to_download.split()[0], lang, api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, max_api_calls)
                  api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s = download_if_needed(word_to_download.split()[1], lang, api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, max_api_calls)
      else:
            for word in word_to_download.split():
                  api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s = download_if_needed(word, lang, api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s, max_api_calls)      
      return api_calls, list_of_already_had_mp3s, list_of_previously_failed_mp3s, list_of_downloaded_mp3s, list_of_not_downloaded_mp3s

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
            raise
            return None
      
      #data = r.json()
      #print(r.content.decode())
      data = json.loads(r.content.decode())
      
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

def DownloadMp3ForAnki(word, lang):
      api_call_count = 1
      with open('apikey.txt') as a:
        APIKEY=a.read()
      lang_dir = os.path.join(pron_fold,lang)
      r = ForvoRequest(word,lang,APIKEY)
      if r:
            api_call_count = 2
            #download a mp3 file, rename it and write it in a costum folder
            #mp3 = requests.get(r[0])    
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
                        print(':) MP3 created',word)
      else:                        
            print(' '*20,':( not available from Forvo', word)
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
