import telebot
import config
import messages


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def greetings(message):
    bot.send_message(message.chat.id, messages.hello)


@bot.message_handler(commands=["language"])
def newsrclan(message):
    msg = bot.send_message(message.chat.id, "What is ur home language?")
    bot.register_next_step_handler(msg, setsrclan)


@bot.message_handler(content_types=['text'])
def text(message):
    if "/" in message.text:
        bot.send_message(message.chat.id, "Incorrect command! Just text /help, if ure lost!")
    else:
        bot.send_message(message.chat.id, "I can do it too!: " + message.text)


def setsrclan(message):
    bot.reply_to(message, "It`s ur new home language!")


bot.infinity_polling()
