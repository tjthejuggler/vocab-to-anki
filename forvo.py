import requests
import urllib
import urllib.parse
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            

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
      
      print(url)

      try:
            #r = requests.get(url)
            r = requests.get(url, headers=headers)

      except:
            raise
            return None
      
      #data = r.json()
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
            




