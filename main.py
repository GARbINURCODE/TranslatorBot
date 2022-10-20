import telebot
import config


bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


bot.infinity_polling()
