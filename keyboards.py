from telebot import types


def hello_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Set languages')
    markup.add(button1)
    return markup


def set_type_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Just text')
    button2 = types.KeyboardButton('A document')
    button3 = types.KeyboardButton('An article from the Internet')
    markup.add(button1, button2, button3)
    return markup


def languages_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('English')
    button2 = types.KeyboardButton('German')
    button3 = types.KeyboardButton('French')
    button4 = types.KeyboardButton('Japanese')
    button5 = types.KeyboardButton('Russian')
    markup.row(button1, button5)
    markup.row(button2, button3, button4)
    return markup