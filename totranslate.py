from googletrans import Translator

translator = Translator()

class TranslatorCl:
    text = ""
    fromlang = ""


    def __init__(self):
        self.text = ""
        self.fromlang = ""
        self.tolang = ""

    def settext(self, t):
        self.text = t

    def setfromlang(self, fl):
        self.fromlang = fl

    def translation(self):
        result = translator.translate(self.text, src=self.fromlang)
        return result.text




