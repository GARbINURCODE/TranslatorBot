from telebot import types


def hello_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Set home language')
    markup.add(button1)
    return markup


def set_type_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Just text')
    button2 = types.KeyboardButton('A document')
    button3 = types.KeyboardButton('An article from the Internet')
    markup.add(button1, button2, button3)
    return markup
