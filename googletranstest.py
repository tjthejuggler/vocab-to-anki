from googletrans import Translator

translator = Translator()
results =translator.translate('hola')
print(results.text)