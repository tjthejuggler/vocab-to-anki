from deep_translator import (GoogleTranslator,MyMemoryTranslator,QCRI,LingueeTranslator)
import os
import os.path
from os import path
import time
from googletrans import Translator



translator_to_use = 'google'

def translate(src_text, dest_langcode, src_langcode):
	global translator_to_use
	src_langcode = 'en'
	dest_langcode = 'tr'
	#print('translator_to_use', translator_to_use)
	cwd = os.getcwd()
	local_dict_file = src_langcode+'_'+dest_langcode+'.json'
	dest_text = ''
	if path.exists(cwd+'/local_dictionaries/'+local_dict_file):			
		with open(cwd+'/local_dictionaries/'+local_dict_file) as json_file:
			local_dict = json.load(json_file)
			if src_text in local_dict:
				dest_text = local_dict[src_text]
	if dest_text == '':
		if translator_to_use == 'google':
			translator_to_use = 'linguee'
			try:
				#print('goog')
				dest_text = GoogleTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
			except:
				pass			
	if dest_text == '':
		if translator_to_use == 'linguee':
			translator_to_use = 'myMemory'
			try:
				#print('lingue')
				dest_text = LingueeTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
			except:
				pass
	if dest_text == '':
		if translator_to_use == 'myMemory':
			translator_to_use = 'pons'
			try:
				#print('myMemory')
				dest_text = MyMemoryTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
			except:
				pass
	if dest_text == '':
		if translator_to_use == 'pons':
			translator_to_use = 'google'
			try:				
				#print('pons')
				dest_text = PonsTranslator(source=src_langcode, target=dest_langcode).translate(src_text)
			except:
				pass
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


translator = Translator()
file = open( "source.txt", "r")
lines = file.readlines()
file.close()

newText = ''
for line in lines:
	if line[0] == '*':
		print(line.rstrip())
	else:
		print(line)
		word_to_define = line.rstrip()
		newText += word_to_define + ' - '
		#print(word_to_define)
		dest_text = ''
		try:
			dest_text = translator.translate(word_to_define, dest='tr', src='en').text
			dest_text = translate_text
			#dest_text = GoogleTranslator(source='en', target='tr').translate(word_to_define)
		except:
			pass
		#dest_text = translate(line, 'tr', 'en')
		myTimer = .5
		while dest_text == '':
			time.sleep(myTimer)
			try:
				dest_text = translator.translate(word_to_define, dest='tr', src='en').text
			except:
				pass
			myTimer = myTimer + myTimer
			if myTimer > 40:
				break
		#print(dest_text)
		print(word_to_define + ' - ' + dest_text)
		newText += dest_text + '\n'

text_file = open("output.txt", "w")
n = text_file.write(newText)
text_file.close()