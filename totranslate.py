import docx
from googletrans import Translator

translator = Translator()


# Class Translator here
class TranslatorCl:
    fromlang = None
    tolang = None

# The Constructor here
    def __init__(self):
        self.fromlang = None
        self.tolang = None

# Setting home language
    def Set_From_Lan(self, fl):
        self.fromlang = fl

    def Set_To_Lan(self, tl):
        self.tolang = tl

# Translation of a text
    def Translation(self, text):
        result = translator.translate(text, src=self.fromlang,
                                      dest=self.tolang)
        return result.text

# The method translates .docx files
# We make a new .docx file and open the one we want to translate
# Read each paragraph in translating file and write translated text in new one
# We should copy a paragraph style too!!!
# Save new file and return its path
    def Docx_Translation(self, file_path):
        doc = docx.Document()
        file = docx.Document(file_path)
        paragraphs = file.paragraphs
        for paragraph in paragraphs:
            if paragraph.text != '':
                translated_text = translator.translate(paragraph.text, src=self.fromlang,
                                                       dest=self.tolang)
                doc.add_paragraph(translated_text.text, paragraph.style.name)
            else:
                doc.add_paragraph(paragraph.text, paragraph.style.name)
        name = 'documents/Translated_text.docx'
        doc.save(name)
        return name

# Translates .txt files
# Just read translating file, translate its text, write translated text in new file
# Save translated file and return its path
    def Txt_Transaltion(self, file_path):
        name = 'documents/Translated_text.txt'
        with open(name, 'w') as translated_file, open(file_path, 'r') as file:
            text = file.read()
            translated_text = translator.translate(text, src=self.fromlang,
                                                   dest=self.tolang)
            translated_file.write(translated_text.text)
            return name

    def Chat_Translation(self, text):
        text = text.lower()
        try:
            result = translator.translate(text, src=self.fromlang,
                                          dest=self.tolang)
            if result.text.lower() == text or translator.detect(text).lang == self.tolang:
                result = translator.translate(text, src=self.tolang,
                                              dest=self.fromlang)
            return result.text.lower()
        except Exception:
            return "I can't translate this text:("

    def forget(self):
        self.fromlang = None
        self.tolang = None
