import docx
from googletrans import Translator
import random

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

    def Translation(self):
        result = translator.translate(self.text, src=self.fromlang)
        return result.text

    def Docx_Translation(self, file_path):
        doc = docx.Document()
        file = docx.Document(file_path)
        paragraphs = file.paragraphs
        for paragraph in paragraphs:
            if paragraph.text != "":
                translated_text = translator.translate(paragraph.text, src='russian')
                doc.add_paragraph(translated_text.text, paragraph.style.name)
            else:
                doc.add_paragraph(paragraph.text, paragraph.style.name)
        name = 'documents/' + str(random.random()) + ".docx"
        doc.save(name)
        return name

    def Txt_Transaltion(self, file_path):
        name = 'documents/' + str(random.random()) + ".txt"
        with open(name, 'w') as translated_file, open(file_path, 'r') as file:
            text = file.read()
            translalted_text = translator.translate(text, src='russian')
            translated_file.write(translalted_text.text)
            return name




