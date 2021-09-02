#input file is formatted
#header
#video
#tr - en - hint
#tr - en - hint
#...

#output file is
#header
#video
#es - tr - en - hint
#tr - en - hint
#...
#from deep_translator import (GoogleTranslator,MyMemoryTranslator,QCRI,LingueeTranslator)
import os
from os import path
import json
import time
#from googletrans import Translator
import six
from google.cloud import translate_v2 as translate

#translator = Translator()


translator_to_use = 'google'
dest_langcode = 'es'
src_langcode = 'en'

def add_translation_to_local_dictionary(src_text, dest_text):
	print('add_translation_to_local_dictionary', dest_text)
	cwd = os.getcwd()
	local_dict_file = dest_langcode+'_'+src_langcode+'.json'
	local_dict = {}
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
	if not src_text in local_dict:
		print('!!!',src_text,dest_text)
		local_dict[src_text] = dest_text
		my_json = json.dumps(local_dict)
		f = open('/home/tim/projects/vocab-to-anki/local_dictionaries/'+local_dict_file,"w")
		f.write(my_json)
		f.close()

# def translate(src_text):
# 	global translator_to_use
# 	print('translator_to_use', translator_to_use)
# 	print('translate', src_text)
# 	cwd = os.getcwd()
# 	local_dict_file = src_langcode+'_'+dest_langcode+'.json'
# 	dest_text = ''
# 	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
# 		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
# 			local_dict = json.load(json_file)
# 			if src_text in local_dict:
# 				dest_text = local_dict[src_text]
# 				print('local dict used', dest_text)
# 	if dest_text == '':
# 		if translator_to_use == 'google':
# 			translator_to_use = 'linguee'
# 			try:
# 				print('goog')
# 				#dest_text = GoogleTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
# 				dest_text = translator.translate(src_text, src = src_langcode, dest=dest_langcode).text
# 			except:
# 				pass			
# 	if dest_text == '':
# 		if translator_to_use == 'linguee':
# 			translator_to_use = 'myMemory'
# 			try:
# 				print('lingue')
# 				dest_text = LingueeTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
# 			except:
# 				pass
# 	if dest_text == '':
# 		if translator_to_use == 'myMemory':
# 			translator_to_use = 'pons'
# 			# try:
# 			# 	print('myMemory')
# 			# 	dest_text = MyMemoryTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
# 			# except:
# 			# 	pass
# 	if dest_text == '':
# 		if translator_to_use == 'pons':
# 			translator_to_use = 'google'
# 			try:				
# 				print('pons')
# 				dest_text = PonsTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
# 			except:
# 				pass
# 	return dest_text

def get_translation_from_local_library(src_text):
	cwd = os.getcwd()
	local_dict_file = dest_langcode+'_'+src_langcode+'.json'
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]
				print('local dict used', dest_text)

	return dest_text

def get_translation(src_text):
	dest_text = get_translation_from_local_library(src_text)

	#print('get_translation',dest_text)
	#if src_text == dest_text or dest_text == '':
	if dest_text == '':
		dest_text = translate_text(dest_langcode, src_text)
	else:
		print('got from local dict', src_text, dest_text)
	if dest_text == '':	
		translation_attempt = 1
		while translation_attempt < 15:
			time.sleep(translation_attempt)
			dest_text = translate_text(dest_langcode, src_text)
			if src_text == dest_text or dest_text == '':
				translation_attempt += translation_attempt
			else:
				translation_attempt = 16
	#if dest_text != '' and src_text != dest_text:	
	if dest_text != '' and dest_text != "None":
		add_translation_to_local_dictionary(src_text, dest_text)
	return dest_text

def translate_text(target, text):
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

    return(format(result["translatedText"]))

file = open( "script_source.txt", "r")
lines = file.readlines()
file.close()


outputlines = []
outputlines.append(lines[0])
outputlines.append(lines[1])
for linenumber in range (2,len(lines)):
	if ' - ' in lines[linenumber]:
		split_line = lines[linenumber].split(' - ')
		outputlines.append('')
		tr_word = split_line[0]
		en_word = split_line[1]
		es_translation = get_translation(en_word)
		if len(split_line) < 3:
			split_line.append('no hint')
		outputlines[linenumber] = es_translation + ' - ' + en_word.rstrip() + ' - ' + tr_word.rstrip() + ', ' + split_line[2].rstrip() +'\n'
		print('outputlines[linenumber]', outputlines[linenumber])
	else:
		if lines[linenumber]:
			tr_translation = get_translation(lines[linenumber].strip())
			if tr_translation:
				outputlines.append('')
				outputlines[linenumber] = tr_translation + ' - ' + lines[linenumber].strip() + ' - no hint\n'

with open('new_source.txt', 'w') as f:
    for item in outputlines:
        f.write("%s" % item)
