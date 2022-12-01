# TranslatorBot
### by [GARbINURCODE](https://github.com/GARbINURCODE)
This project boostraped with [Python 3.9](https://www.python.org/downloads/release/python-390/).
A simple python translator bot for Telegram.
It can translate text, documents and web-pages.
The bot uses the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).
## Features

- **Translation of text messages** 

    For this you need to send a message to the bot. 
    For realization of this feature, the bot uses the 
    [googletrans-py](https://cloud.google.com/translate/docs/setup) library.
    It`s a free and unlimited API for Google Translate.
    Translating text messages is available in 103 languages, but there are only 5 in the bot:
    - English
    - Russian
    - German
    - French
    - Polish
    - Japanese

- **Translation of .txt files** 

     For this you need to send a .txt file to the bot. 
     The bot will translate the text in the file and send it back to you.
     To download file from Telegram, the bot uses the byte-reading method.
     The text in the file is rewrites in the same file.
     Later we make a new file with the translated text.

- **Translation of .docx files** 
    
    This feature is similar to the previous one.
    However, the bot uses the [python-docx](https://python-docx.readthedocs.io/en/latest/) library to work with .docx files.
    The bot translates the text in the file and sends it back to you.

- **Translation of web-pages**
  
    To translate web-pages, the bot have to srap them.
    For scrapping the bot uses the [requests](https://docs.python-requests.org/en/master/) and 
    [beatifulsoup4](https://pypi.org/project/beautifulsoup4/) library. 
    We get and translate the title and context(/p) of the page.
    The bot sends the translated text to you.
    There is a loop for sending the text in parts, because the bot can`t send more than 4096 characters.

- **Translation of messages in group chats**
  
    The aim of this feature is to allow users to communicate in different languages.
    I guess, this project is not the best way to do it, but it works and 
    our team is trying to improve it and help people to break the language barrier.
    Using this feature, the bot translates messages in group chats and sends them to the user.
    Nota bene: the bot translates messages it both ways: from the 1st language to the 2nd one
    and from the 2nd language to the 1st one.
> **Note:** The bot is still in development. There are a lot of problems
> in translating from Japanese and Russian. We`d reccoemend you not to use them.
## Usage
- [googletrans-py](https://cloud.google.com/translate/docs/setup)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [beatifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [python-docx](https://pypi.org/project/python-docx/)
