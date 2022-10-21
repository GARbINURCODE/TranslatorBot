import telebot
import config
import messages
import totranslate


bot = telebot.TeleBot(config.token)
translation = totranslate.TranslatorCl()


@bot.message_handler(commands=["start"])
def greetings(message):
    bot.send_message(message.chat.id, messages.hello)


@bot.message_handler(commands=["language"])
def newdestlan(message):
    msg = bot.send_message(message.chat.id, "What is ur home language?")
    bot.register_next_step_handler(msg, setdestlan)


@bot.message_handler(commands=["totranslate"])
def newtext(message):
    msg = bot.send_message(message.chat.id, "Print text for translation?")
    bot.register_next_step_handler(msg, settext)


@bot.message_handler(content_types=["text"])
def text(message):
    if "/" in message.text:
        bot.send_message(message.chat.id, "Incorrect command! Just text /help, if ure lost!")
    else:
        bot.send_message(message.chat.id, "I can do it too!: " + message.text)


def setdestlan(message):
    translation.setfromlang(message.text)
    bot.reply_to(message, "It`s ur new home language!")

def settext(message):
    translation.settext(message.text)
    bot.send_message(message.chat.id, translation.translation())


bot.infinity_polling()
