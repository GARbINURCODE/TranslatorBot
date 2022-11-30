import telebot
import keyboards
import config
import totranslate
import os
import scraper

# Some objects of classes that we need
bot = telebot.TeleBot(config.token)
translator = totranslate.TranslatorCl()


# Command start handler and the suggestion to set home language in markup
# Bot is divided into two parts: chat and translator
# In chat we can set languages and translate text of the other user
# It is needed to communicate without language barrier
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type == 'private':
        msg = bot.send_message(message.chat.id, f"Hi, {message.from_user.first_name}. "
                                                f"I`m a translator bot. "
                                                f"Do u want to translate something?",
                               reply_markup=keyboards.hello_markup())
        bot.register_next_step_handler(msg, hello_markup_handler)
    else:
        msg = bot.reply_to(message, f'Hi everybody.'
                                    f'I`m a translator bot. '
                                    f'I can help u to communicate with each other.'
                                    f'Please, choose ur language.'
                                    f'If u`re going to use language,'
                                    f'it`s strongly recommended to set it first.',
                           reply_markup=keyboards.languages_markup())
        bot.register_next_step_handler(msg, languages_markup_handler)


# The handler of the markup u can see above in private part
@bot.message_handler(content_types=["text"])
def hello_markup_handler(message):
    for file in os.listdir('documents'):
        os.remove('documents/' + file)
    if message.text == 'Set languages':
        translator.forget()
        msg = bot.send_message(message.chat.id, "What is the language of this text?",
                               reply_markup=keyboards.languages_markup())
        bot.register_next_step_handler(msg, languages_markup_handler)
    elif message.text == 'Stop':
        translator.forget()
        msg = bot.send_message(message.chat.id, 'Ok, bye!',
                               reply_markup=keyboards.start_markup())
        bot.register_next_step_handler(msg, start)


# The handler of the markup u can see above
# We set home language and ask what do u want to translate in private part
# We set the languages of users in chat part
@bot.message_handler(content_types=["text"])
def languages_markup_handler(message):
    if translator.from_lang is None:
        translator.set_from_lan(message.text.lower())
        if message.chat.type == 'private':
            bot.send_message(message.chat.id, "It`s ur home language!")
            msg = bot.send_message(message.chat.id, "What is the language u want to get this text in?",
                                   reply_markup=keyboards.languages_markup())
        else:
            msg = bot.send_message(message.chat.id, "What is the language of ur fellow?",
                                   reply_markup=keyboards.languages_markup())
        bot.register_next_step_handler(msg, languages_markup_handler)
    else:
        translator.set_to_lan(message.text.lower())
        if message.chat.type == 'private':
            bot.send_message(message.chat.id, "It`s ur new language!")
            msg = bot.send_message(message.chat.id, 'What type of text u want to translate?',
                                   reply_markup=keyboards.set_type_markup())
            bot.register_next_step_handler(msg, set_type_markup_handler)
        else:
            msg = bot.send_message(message.chat.id, "It`s ur fellow`s language!",
                                   reply_markup=keyboards.chat_markup())
            bot.register_next_step_handler(msg, chat_handler)


# The handler is needed to set the type of translation: text or file or url
def set_type_markup_handler(message):
    if message.text == 'Just a text':
        msg = bot.send_message(message.chat.id, 'Please, print the text in your language:')
        bot.register_next_step_handler(msg, text_handler)
    elif message.text == 'A document':
        msg = bot.send_message(message.chat.id, 'Please, send you docx or txt file:')
        bot.register_next_step_handler(msg, docs_handler)
    elif message.text == 'An article from the Internet':
        msg = bot.send_message(message.chat.id, 'Please, send the link:')
        bot.register_next_step_handler(msg, url_handler)
    else:
        msg = bot.send_message(message.chat.id, 'Ok, let`s start again.',
                               reply_markup=keyboards.hello_markup())
        bot.register_next_step_handler(msg, hello_markup_handler)


# We use TranslatorCl object to translate user`s text
# And we send it back
# If user wants to translate something else, we repeat the loop
@bot.message_handler(content_types=["text"])
def text_handler(message):
    bot.send_message(message.chat.id, translator.translate(message.text))
    msg = bot.send_message(message.chat.id, 'What do u want to translate next?',
                           reply_markup=keyboards.hello_markup())
    bot.register_next_step_handler(msg, hello_markup_handler)


# We use TranslatorCl object to translate .docx and .txt files there
# An exception is needed because translating of file can make some problems
@bot.message_handler(content_types=["document"])
def docs_handler(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.chat.id, "Please, wait a sec...")
        with open(file_info.file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        doc = None
        if file_info.file_path.endswith(".docx"):
            doc = translator.translate_docx(file_info.file_path)
        elif file_info.file_path.endswith(".txt"):
            doc = translator.translate_txt(file_info.file_path)
        file = open(doc, 'rb')
        bot.send_document(message.chat.id, file)
        file.close()
        msg = bot.send_message(message.chat.id, 'What do u want to translate next?',
                               reply_markup=keyboards.hello_markup())
        bot.register_next_step_handler(msg, hello_markup_handler)
    except Exception:
        print("Docs_Handler Error - Try again after 5 secs")
        msg = bot.send_message(message.chat.id, "Ooops, something gone wrong. "
                                                "Try to send me another file."
                                                "Or choose another language.",
                               reply_markup=keyboards.hello_markup())
        bot.register_next_step_handler(msg, hello_markup_handler)


# We use TranslatorCl object to translate the text from the url
# Also we use scraper module to get the text from the url
# There is a loop because translating of url can take a lot of time
# Therefore we send translated paragraphs one by one
@bot.message_handler(content_types=["text"])
def url_handler(message):
    try:
        url_scraper = scraper.ScraperCl(message.text)
        if url_scraper.soup is not None:
            bot.send_message(message.chat.id, translator.translate(url_scraper.get_title()))
            for i in url_scraper.get_content():
                bot.send_message(message.chat.id, translator.translate(i))
            msg = bot.send_message(message.chat.id, "Do u want to translate something else?",
                                   reply_markup=keyboards.hello_markup())
            bot.register_next_step_handler(msg, hello_markup_handler)
        else:
            msg = bot.send_message(message.chat.id, "There is no url! "
                                                    "Please, send me a real link.")
            bot.register_next_step_handler(msg, url_handler)
    except Exception:
        print("Url_Handler Error - Try again after 5 secs")
        msg = bot.send_message(message.chat.id, "Ooops, something gone wrong. "
                                                "Try to send me another link."
                                                "Or maybe it`s not a link at all."
                                                "Or choose another language.",
                               reply_markup=keyboards.hello_markup())
        bot.register_next_step_handler(msg, hello_markup_handler)


# We use TranslatorCl object to translate user`s text
# Mostly this def is markup handler
@bot.message_handler(content_types=["text"])
def chat_handler(message):
    if message.text == 'Set languages':
        translator.forget()
        msg = bot.send_message(message.chat.id, "What is ur language?",
                               reply_markup=keyboards.languages_markup())
        bot.register_next_step_handler(msg, languages_markup_handler)
    elif message.text == 'Stop':
        translator.forget()
        msg = bot.send_message(message.chat.id, "Ok, bye!",
                               reply_markup=keyboards.start_markup())
        bot.register_next_step_handler(msg, start)
    else:
        msg = bot.reply_to(message, translator.translate_for_chat(message.text))
        bot.register_next_step_handler(msg, chat_handler)


# A stuff for bot working
bot.infinity_polling()
