import telebot
import keyboards
import config
import messages
import totranslate


bot = telebot.TeleBot(config.token)
translator = totranslate.TranslatorCl()
keyboard = keyboards.KeyboardCl()


@bot.message_handler(commands=["start"])
def start(message):
    msg = bot.send_message(message.chat.id, messages.hello,
                           reply_markup=keyboard.hello_markup())
    bot.register_next_step_handler(msg, hello_markup_handler)


@bot.message_handler(content_types=["text"])
def hello_markup_handler(message):
    if message.text == 'Set home language':
        msg = bot.send_message(message.chat.id, "What is ur home language?")
        bot.register_next_step_handler(msg, set_home_lan)

def set_home_lan(message):
    translator.setfromlang(message.text)
    bot.reply_to(message, "It`s ur new home language!")
    msg = bot.send_message(message.chat.id, "What do u want to translate?",
                           reply_markup=keyboard.set_type_markup())
    bot.register_next_step_handler(msg, set_type_markup_handler)

def set_type_markup_handler(message):
    if message.text == 'Just text':
        msg = bot.send_message(message.chat.id, 'Please, print the text in your language:')
        bot.register_next_step_handler(msg, set_text)
    else:
        msg = bot.send_message(message.chat.id, 'Please, send you docx or txt file:')
        bot.register_next_step_handler(msg, docs_handler)

@bot.message_handler(content_types=["text"])
def set_text(message):
    translator.settext(message.text)
    msg = bot.send_message(message.chat.id, translator.Translation(),
                           reply_markup=keyboard.hello_markup())
    bot.register_next_step_handler(msg, hello_markup_handler)


@bot.message_handler(content_types=["document"])
def docs_handler(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_info.file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
        doc = ''
        if file_info.file_path.endswith(".docx"):
            doc = translator.Docx_Translation(file_info.file_path)
        elif file_info.file_path.endswith(".txt"):
            doc = translator.Txt_Transaltion(file_info.file_path)
        file = open(doc, 'rb')
        msg = bot.send_document(message.chat.id, file,
                                reply_markup=keyboard.hello_markup())
        file.close()
        bot.register_next_step_handler(msg, hello_markup_handler)
    except Exception:
        print(Exception)

bot.infinity_polling()
