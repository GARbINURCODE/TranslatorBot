import telebot
import keyboards
import config
import totranslate
import time
import scraper

# Some objects of classes that we need
bot = telebot.TeleBot(config.token)
translator = totranslate.TranslatorCl()


# Command start handler and the suggestion to set home language in markup
@bot.message_handler(commands=["start"])
def start(message):
    msg = bot.send_message(message.chat.id, f"Hi, {message.from_user.first_name}. "
                                            f"I`m a translator bot. "
                                            f"Do u want to translate something?",
                           reply_markup=keyboards.hello_markup())
    bot.register_next_step_handler(msg, hello_markup_handler)


# The handler of the markup u can see above
@bot.message_handler(content_types=["text"])
def hello_markup_handler(message):
    if message.text == 'Set home language':
        msg = bot.send_message(message.chat.id, "What is ur home language?")
        bot.register_next_step_handler(msg, set_home_lan)


# Setting new home language
# Suggestion to choose if we want to translate a text or a document
# For the suggestion we use the other markup
def set_home_lan(message):
    translator.Set_From_Lan(message.text)
    bot.reply_to(message, "It`s ur new home language!")
    msg = bot.send_message(message.chat.id, "What do u want to translate?",
                           reply_markup=keyboards.set_type_markup())
    bot.register_next_step_handler(msg, set_type_markup_handler)


# The handler of the markup u can see above
def set_type_markup_handler(message):
    if message.text == 'Just text':
        msg = bot.send_message(message.chat.id, 'Please, print the text in your language:')
        bot.register_next_step_handler(msg, text_handler)
    elif message.text == 'A document':
        msg = bot.send_message(message.chat.id, 'Please, send you docx or txt file:')
        bot.register_next_step_handler(msg, docs_handler)
    else:
        msg = bot.send_message(message.chat.id, 'Please, send the link:')
        bot.register_next_step_handler(msg, url_handler)


# We use TranslatorCl object to translate this text
@bot.message_handler(content_types=["text"])
def text_handler(message):
    msg = bot.send_message(message.chat.id, translator.Translation(message.text),
                           reply_markup=keyboards.hello_markup())
    bot.register_next_step_handler(msg, hello_markup_handler)


# We use TranslatorCl object to translate .docx and .txt files there
# An exception because translating of file can make some problems
@bot.message_handler(content_types=["document"])
def docs_handler(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.chat.id, "Please, wait a sec...")
        with open(file_info.file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        doc = ''
        if file_info.file_path.endswith(".docx"):
            doc = translator.Docx_Translation(file_info.file_path)
        elif file_info.file_path.endswith(".txt"):
            doc = translator.Txt_Transaltion(file_info.file_path)
        file = open(doc, 'rb')
        msg = bot.send_document(message.chat.id, file,
                                reply_markup=keyboards.hello_markup())
        file.close()
        bot.register_next_step_handler(msg, hello_markup_handler)
    except OSError:
        print("Docs_Handler Error - Try again after 5 secs")
        time.sleep(5)
        msg = bot.send_message(message.chat.id, "Ooops, something gone wrong. "
                                                "Try to send me another file.",
                               reply_markup=keyboards.set_type_markup())
        bot.register_next_step_handler(msg, set_type_markup_handler)


# We use TranslatorCl object to translate the text from the url
# Also we use scraper module to get the text from the url
@bot.message_handler(content_types=["text"])
def url_handler(message):
    try:
        url_scraper = scraper.ScraperCl(message.text)
        if url_scraper.soup is not None:
            msg = bot.send_message(message.chat.id, translator.Translation(url_scraper.get_title()))
            for i in url_scraper.get_content():
                bot.send_message(message.chat.id, translator.Translation(i))
            bot.register_next_step_handler(msg, hello_markup_handler)
        else:
            msg = bot.send_message(message.chat.id, "There is no url! "
                                                    "Please, send me a real link.")
            bot.register_next_step_handler(msg, url_handler)
    except OSError:
        print("Url_Handler Error - Try again after 5 secs")
        time.sleep(5)
        msg = bot.send_message(message.chat.id, "Ooops, something gone wrong. "
                                                "Try to send me another link.",
                               reply_markup=keyboards.set_type_markup())
        bot.register_next_step_handler(msg, set_type_markup_handler)




# A stuff for bot working
bot.infinity_polling()
