# vocab-to-anki
inputs list of word foreign language words in source.txt and translates them, downloads/synthesizes their pronunciations, and makes anki decks or audio lessons out of them.

this is a command line tool and uses the following options:

"language1", help="first language code (en = english)"
"-2", "--language2", help="second language code (en = english)"
"-d", "--download", type = int,
							help="should download pronunciations from forvo, \
							number of languages to download, max number of api calls"
"-l", "--linesmax", type = int,
							help="maximum number of lines to be processed"
"-x", "--maxapis", type = int,
							help="maximum number of api calls allowed"
"-k", "--apkgsource", help="use apkg file as source, \
							name of apkg file to use"
"-c", "--reducedapkg", action="store_true", help="reduce the number of words in the apkg"
"-t", "--translate", action="store_true",help="translate words and output formatted list"
"-m", "--makeankideck", action="store_true",help="make an anki deck from formatted list"
"-ma", "--makeankideckaudio", action="store_true",help="make an anki deck from formatted \
						list that is audio only"
"-a", "--audiolesson", action="store_true",help="make audio lesson from formatted list"
"-r", "--randomorder", action="store_true",help="randomize the order of the words being processed"
"-q", "--requireindivwords", action="store_true",help="only make an audio lesson entry if all \
							individual words have been downloaded"
"-s", "--skipconfirmation", action="store_true",help="skip confirmation prompt"
"-hn", "--hinttranslation", help="language code to be used in hint translation"
"-p", "--alternatepronunciations", type = int, 
							help="the number of alternate pronuciations to download"
"-f", "--firststring", help="the first string in the source list that will be recognized"
"-g", "--addankitag", help="tag to be added to any anki deck"

first language is required

example:
python3 main.py es -2 en -t  :  takes a list of spanish words and gets their english translations 

