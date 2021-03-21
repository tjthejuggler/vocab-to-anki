def get_lines_from_source(deck_name, only_get_anki_cards_being_worked_on, use_anki_file, should_make_anki_deck_audio_only, max_lines):
	lines = []
	url = ''
	if use_anki_file:
		print("deck_name", deck_name)
		lines, new_deck_name = get_word_list_from_apkg(deck_name, only_get_anki_cards_being_worked_on, should_make_anki_deck_audio_only, max_lines)
		print('lines', lines)
	else:	
		file = open( "source.txt", "r")
		lines = file.readlines()
		file.close()
		new_deck_name = lines[0].replace(' ','_').strip()
		url = lines[1]
		lines = lines[2:]
	return lines, new_deck_name, url

def get_word_list_from_apkg(filename, only_get_anki_cards_being_worked_on, should_make_anki_deck_audio_only, max_lines):
	with zipfile.ZipFile(filename+".apkg", 'r') as zip_ref:
		zip_ref.extractall(cwd+"/unzipped_apkg/"+filename)
	new_deck_name = filename
	if should_make_anki_deck_audio_only:
		new_deck_name = new_deck_name + 'Only'
	accepted_cards = []
	connection = sqlite3.connect(cwd+"/unzipped_apkg/"+filename+"/collection.anki2")  # connect to your DB
	cursor = connection.cursor()  # get a cursor
	cursor.execute("SELECT nid,ivl,due,factor FROM cards")  # execute a simple SQL select query
	card_selection = cursor.fetchall()  # get all the results from the above query
	for nid,ivl,due,factor in card_selection:
		cursor2 = connection.cursor()
		cursor2.execute("SELECT flds FROM notes WHERE id="+str(nid))
		flds_selection = cursor2.fetchall()
		fld = ' '.join(flds_selection[0])
		split_fld = fld.split('\x1f')
		print('split_fld', split_fld)
		word = ''
		translation = ''
		hint = ''
		using_audio_only_apkg = False
		if ' - ' in split_fld[4]:
			using_audio_only_apkg = True
		if using_audio_only_apkg:			
			word = split_fld[4].split(' - ')[0]
			translation = split_fld[4].split(' - ')[1]
			print('word',word)
			hint = 'no hint'
			if '\n' in split_fld[2]:
				hint = split_fld[2].split('\n')[1]
			elif '<br>' in split_fld[2]:
				hint = split_fld[2].split('<br>')[1]
			print('translation',translation)
			print('hint', hint)
		else:
			split_fld = fld.split('\x1f')
			word = re.sub("[\(\[].*?[\)\]]", "", split_fld[0]).strip()
			translation = split_fld[1]
			hint = split_fld[2]	
		card_info = [word, translation, hint, ivl, factor]
		if only_get_anki_cards_being_worked_on:
			if ivl == 0 and due > 10000:
				accepted_cards.append(card_info)
			if ivl != 0 and ivl < 5:
				accepted_cards.append(card_info)			
				#print('word:',word,' translation:',translation,' ivl:',ivl,' due:',due,' factor:',factor)
		else:
			accepted_cards.append(card_info)
	#print(accepted_cards)
	accepted_cards = sorted(accepted_cards, key=itemgetter(2))
	print('--------------------')
	#print(accepted_cards)
	print('!!!!!!!')
	accepted_cards = accepted_cards[:max_lines]
	print(accepted_cards)
	lines_to_return = []
	for accepted_card in accepted_cards:
		new_card = accepted_card[0]+' - '+accepted_card[1]+' - '+accepted_card[2]
		if not new_card in lines_to_return:
			lines_to_return.append(new_card)
	return lines_to_return, new_deck_name

def determine_if_formatted(lines):
	percent_formatted = 0
	formatted_line_count = 0
	is_formatted = True
	for line in lines:
		if ' - ' in line:
			formatted_line_count+=1
	if len(lines) != 0:	
		percent_formatted = formatted_line_count / len(lines)
	if percent_formatted < .9:
		is_formatted = False
	return is_formatted