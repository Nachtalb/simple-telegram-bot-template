# Simple Telegram Bot Template

This little `bot.py` acts as a python based telegram bot.

Simply install the requirements with `pip install -r requirements.txt` and put your token that you
got from [@BotFather](https://t.me/BotFater) in the `TOKEN` variable near the top. After that you
are good to go. Start the bot with `python bot.py`.

To add commands etc. you have to add a method to the `TelegramBot` class and use the decorator
`@command`. If don't call the decorator it will by default create a `CommandHandler` with your
method name as `/name` in telegram. By default there is a `/start` handler an error handler and
MessageHandlder that returns the sent message (but without newlines, ... cuz why not).

This template is compatible with python 3.8 (and up but not tested) and has no license whatsoever so
you can do anything you want with it.
