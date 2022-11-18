import telebot
from telebot import types
import config
import messages
import totranslate


bot = telebot.TeleBot(config.token)
translator = totranslate.TranslatorCl()


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Translate text')
    button2 = types.KeyboardButton('Translate document')
    markup.add(button1, button2)

    bot.send_message(message.chat.id, messages.hello
                     , reply_markup=markup)


@bot.message_handler(commands=["translate"])
def newdestlan(message):
    msg = bot.send_message(message.chat.id, "What is ur home language?")
    bot.register_next_step_handler(msg, setdestlan)


@bot.message_handler(content_types=["text"])
def keyboard_handler(message):
    if message.text == 'Translate text':
        msg = bot.send_message(message.chat.id, "What is ur home language?")
        bot.register_next_step_handler(msg, setdestlan)
    elif message.text == 'Translate document':
        msg = bot.send_message(message.chat.id, "Send me your .docx or .txt file:")
        bot.register_next_step_handler(msg, handle_docs)

@bot.message_handler(content_types=["text"])
def setdestlan(message):
    translator.setfromlang(message.text)
    bot.reply_to(message, "It`s ur new home language!")
    msg = bot.send_message(message.chat.id, "Print text for translation")
    bot.register_next_step_handler(msg, settext)


@bot.message_handler(content_types=["text"])
def settext(message):
    translator.settext(message.text)
    bot.send_message(message.chat.id, translator.Translation())


@bot.message_handler(content_types=["text"])
def text(message):
    if "/" in message.text:
        bot.send_message(message.chat.id, "Incorrect command! Just text /help, if ure lost!")
    else:
        bot.send_message(message.chat.id, "I can do it too!: " + message.text)


@bot.message_handler(content_types=["document"])
def handle_docs(message):
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
        bot.send_document(message.chat.id, file)
        file.close()
    except Exception:
        print(Exception)

bot.infinity_polling()
