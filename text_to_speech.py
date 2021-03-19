from google.cloud import texttospeech
import os
from pathlib import Path

home = str(Path.home())
pron_fold = home+'/pronunciations'

def synthesize_text(text, lang):
    """Synthesizes speech from the input string of text."""
    lang_code = "en-US"
    nm = "en-US-Standard-C"
    sgen = texttospeech.SsmlVoiceGender.FEMALE
    if lang == 'tr':
        lang_code = "tr-TR"
        nm = "tr-TR-Standard-B"
        sgen = texttospeech.SsmlVoiceGender.MALE
    elif lang == 'en':
        lang_code = "en-US"
        nm = "en-US-Standard-C"
        sgen = texttospeech.SsmlVoiceGender.FEMALE      
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        name=nm,
        ssml_gender=sgen,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    lang_dir = os.path.join(pron_fold,lang)
    file_name = text.replace('\n','')+'.mp3'
    file_path = os.path.join(lang_dir, file_name)
    with open(file_path, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file')

synthesize_text("şahsen konuşmak benim için zor", "tr")