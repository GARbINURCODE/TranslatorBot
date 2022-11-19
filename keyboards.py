from telebot import types

class KeyboardCl:
    def hello_markup(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton('Set home language')
        markup.add(button1)
        return(markup)

    def set_type_markup(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton('Just text')
        button2 = types.KeyboardButton('A document')
        markup.add(button1, button2)
        return (markup)