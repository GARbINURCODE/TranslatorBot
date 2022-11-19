import docx
from googletrans import Translator

translator = Translator()

class TranslatorCl:
    text = ""
    fromlang = ""
    tolang = ''

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
                translated_text = translator.translate(paragraph.text, src=self.fromlang)
                doc.add_paragraph(translated_text.text, paragraph.style.name)
            else:
                doc.add_paragraph(paragraph.text, paragraph.style.name)
        name = 'documents/Translated_text.docx'
        doc.save(name)
        return name

    def Txt_Transaltion(self, file_path):
        name = 'documents/Translated_text.txt'
        with open(name, 'w') as translated_file, open(file_path, 'r') as file:
            text = file.read()
            translated_text = translator.translate(text, src=self.fromlang)
            translated_file.write(translated_text.text)
            return name




