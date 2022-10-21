from googletrans import Translator

translator = Translator()

print(translator.translate('Привет', dest='en', src='ru'))
