# vocab-to-anki
converts text files to anki cards

main.py - creates an anki deck from a list of vocab in the format. this can be used for foreign words i don't want pronunciations of, or non foreign word decks
foreign word/phrase - translation - hint

mainaudio.py does the same thing, but it also uses a paid forvo APIkey to download and add an mps of the pronunciation of . the foreign word. it only does pronunciations for single words, and right now it is hard coded to do turkish.

