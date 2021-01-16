from deep_translator import (GoogleTranslator,MyMemoryTranslator,QCRI,LingueeTranslator)
import os
import os.path
from os import path
import time

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

file = open( "source.txt", "r")
lines = file.readlines()
file.close()

newText = ''
for line in lines:
	if line[0] == '*':
		print(line.rstrip())
	else:
		word_to_define = line.rstrip()
		newText += word_to_define + ' - '
		#print(word_to_define)
		dest_text = ''
		try:
			dest_text = GoogleTranslator(source='en', target='tr').translate(word_to_define)
		except:
			pass
		#dest_text = translate(line, 'tr', 'en')
		myTimer = .5
		while dest_text == '':
			time.sleep(myTimer)
			try:
				dest_text = GoogleTranslator(source='en', target='tr').translate(word_to_define)
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