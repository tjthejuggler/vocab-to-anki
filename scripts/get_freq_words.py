#split every line on punctuation
#if a line has more than 3 words, put every word on its own line
#count the occurence of every line
#remove the most common words in the language
#make a list of the most frequent words in the show

#todo
#make something that deletes the first X number of 

from wordfreq import zipf_frequency
import re
from collections import Counter
file = open( "script_source.txt", "r")
lines = file.readlines()
file.close()

words_to_ignore = ['arturo','raquel','tabii','tamam','laura','biliyorum','polis','profesör',\
					'bilmiyorum', 'üzgünüm', 'alison', 'beş', 'berlin', 'helsinki', 'buraya',\
					'denver','misin', 'musun','biliyor', 'yedi', 'değilim','tabii ki','sekiz',\
					'rio', 'hey', 'dokuz', 'altı', 'değildi', 'anne', 'dün', 'seninle','pardon',\
					'mesaj','miyim','baba','on','annem','git','görmek', 'misiniz','onları',\
					'söyledi','tane','affedersiniz','hepsi','benimle','metre','araba','biliyor musun',\
					'kahve','kızı','geliyorum','otur','nerede','bekle','sevindim','geldim', 'babam']

# PUNCT_RE = regex.compile(r'(\p{Punctuation})')    

# print(PUNCT_RE.split(test_data))


punc_split_lines = []
for line in lines:
	line = (re.sub(r"[^\w\d'\s]",'@',line))
	#line = line.strip()
	#if line != '\n':
	line = line.strip()
	if line.strip() and line != '\n' and line:
		print(line)
		if ("@") in line:
			split_line = line.split("@")
			for phrase in split_line:
				#if phrase != '\n':
				if phrase.strip() and phrase != '\n' and phrase.strip():
					punc_split_lines.append(phrase)
		else:
			punc_split_lines.append(line)

print(punc_split_lines)

no_long_lines = []
for line in punc_split_lines:
	if len(line.split()) > 4:
		print('long line', line)
		print(len(line))
		for word in line.split():
			no_long_lines.append(word)
	else:
		print(line)
		no_long_lines.append(line)

no_punc_lower = []
for line in no_long_lines:
	if len(line) > 2:
		no_punc_lower.append(line.lower().strip())

remove_ignore_words = []
for line in no_punc_lower:
	if line not in words_to_ignore:
		remove_ignore_words.append(line)

remove_freq_words = []
for line in remove_ignore_words:
	if len(line.split()) == 1:
		word_src_freq = zipf_frequency(line, "tr")
		if word_src_freq < 5.5:
			if word_src_freq > 1:
				remove_freq_words.append(line)
				print(word_src_freq, line)

remove_freq_phrases = []
for line in remove_ignore_words:
	if len(line.split()) > 1:
		word_src_freq = zipf_frequency(line, "tr")
		if word_src_freq < 5.5:
			if word_src_freq > 1:
				remove_freq_phrases.append(line)
				print(word_src_freq, line)



Counter_phrases = Counter(remove_freq_phrases)
most_occur_phrases = Counter_phrases.most_common(100)

Counter_words = Counter(remove_freq_words)

most_occur_words = Counter_words.most_common(100)

print(most_occur_words)
print(most_occur_phrases)


most_occur_words_only = [i[0] for i in most_occur_words]

most_occur_phrases_only = [i[0] for i in most_occur_phrases]

	# for n in re.findall(r'[\u4e00-\u9fff]+', line):
	# 	outputlines.append(n)

most_occur_everything = most_occur_words_only + most_occur_phrases_only
#print(most_occur_everything)
with open('new_source.txt', 'w') as f:
    for item in most_occur_everything:
        f.write("%s" % item+'\n')

#string = "the •  word"
