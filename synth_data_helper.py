from google.cloud import texttospeech

def get_synth_data(lang):
	lang_code = ''
	nm = ''
	sgen = texttospeech.SsmlVoiceGender.FEMALE
	if lang == 'tr':
		lang_code, nm, sgen = "tr-TR","tr-TR-Standard-B",texttospeech.SsmlVoiceGender.MALE
	elif lang == 'en':
		lang_code, nm, sgen = "en-US","en-US-Standard-C",texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'da':
		lang_code, nm, sgen = "da-DK","da-DK-Standard-C",texttospeech.SsmlVoiceGender.MALE
	elif lang == 'nl':
		lang_code, nm, sgen = "nl-NL", "nl-NL-Standard-C", texttospeech.SsmlVoiceGender.MALE
	elif lang == 'ar':
		lang_code, nm, sgen = 'ar-XA', 'ar-XA-Standard-D', texttospeech.SsmlVoiceGender.FEMALE	
	elif lang == 'bn':
		lang_code, nm, sgen = 'bn-IN', 'bn-IN-Standard-B', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'cs':
		lang_code, nm, sgen = 'cs-CZ', 'cs-CZ-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'de':
		lang_code, nm, sgen = 'de-DE', 'de-DE-Standard-E', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'es':
		lang_code, nm, sgen = 'es-ES', 'es-ES-Standard-B', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'fr':
		lang_code, nm, sgen = 'fr-FR', 'fr-FR-Standard-D', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'hi':
		lang_code, nm, sgen = 'hi-IN', 'hi-IN-Standard-C', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'ind':
		lang_code, nm, sgen = 'id-ID', 'id-ID-Standard-B', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'it':
		lang_code, nm, sgen = 'it-IT', 'it-IT-Standard-C', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'ko':
		lang_code, nm, sgen = 'ko-KR', 'ko-KR-Standard-C', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'ru':
		lang_code, nm, sgen = 'ru-RU', 'ru-RU-Standard-D', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'th':
		lang_code, nm, sgen = 'th-TH', 'th-TH-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'zh':
		lang_code, nm, sgen = 'yue-HK', 'yue-HK-Standard-B', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'fi':
		lang_code, nm, sgen = 'fi-FI', 'fi-FI-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'el':
		lang_code, nm, sgen = 'el-GR', 'el-GR-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'hu':
		lang_code, nm, sgen = 'hu-HU', 'hu-HU-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'ja':
		lang_code, nm, sgen = 'ja-JP', 'ja-JP-Standard-C', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'no':
		lang_code, nm, sgen = 'nb-NO', 'nb-NO-Standard-B', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'pl':
		lang_code, nm, sgen = 'pl-PL', 'pl-PL-Standard-C', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'pt':
		lang_code, nm, sgen = 'pt-PT', 'pt-PT-Standard-B', texttospeech.SsmlVoiceGender.MALE
	elif lang == 'ro':
		lang_code, nm, sgen = 'ro-RO', 'ro-RO-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'sk':
		lang_code, nm, sgen = 'sk-SK', 'sk-SK-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'sv':
		lang_code, nm, sgen = 'sv-SE', 'sv-SE-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'uk':
		lang_code, nm, sgen = 'uk-UA', 'uk-UA-Standard-A', texttospeech.SsmlVoiceGender.FEMALE
	elif lang == 'vi':
		lang_code, nm, sgen = 'vi-VN', 'vi-VN-Standard-D', texttospeech.SsmlVoiceGender.MALE		 	 	
	return lang_code, nm, sgen

#data doesn't exist
#af, bg, sq