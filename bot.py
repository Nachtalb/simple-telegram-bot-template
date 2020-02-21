from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, Update

from typing import Callable

import re
import logging

logging.basicConfig(format='%(asctime)s = %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = ''
updater = Updater(TOKEN)
dispatcher = updater.dispatcher


def command(names=None, handler=None, filters=None, is_error=False, *wargs, **wkwargs):
    def outer_wrapper(func):
        nonlocal names, handler, filters, is_error, wargs, wkwargs

        def inner_wrapper(self_or_bot, *args, **kwargs):
            if isinstance(self_or_bot, TelegramBot):
                return func(self_or_bot, *args, **kwargs)

            args = list(args)
            instance = TelegramBot(self_or_bot, args.pop(0))
            return func(instance, *args, **kwargs)

        if not names:
            names = [func.__name__]
        elif isinstance(names, str):
            name = [names]

        if is_error:
            dispatcher.add_error_handler(inner_wrapper)
        elif handler == CommandHandler or not handler:
            dispatcher.add_handler(CommandHandler(names, inner_wrapper, filters=filters, *wargs, **wkwargs))
        elif handler == MessageHandler:
            dispatcher.add_handler(MessageHandler(filters, callback=inner_wrapper, *wargs, **wkwargs))

        return inner_wrapper

    if isinstance(names, Callable):
        func, names = names, None
        return outer_wrapper(func)
    return outer_wrapper


class TelegramBot:
    def __init__(self, bot: Bot, update: Update):
        self.bot = bot
        self.update = update
        self.message = update.effective_message
        self.user = update.effective_user
        self.chat = update.effective_chat
        self.logger = logging.getLogger(self.__class__.__name__)

    def reply(self, *args, **kwargs):
        self.message.reply_text(*args, **kwargs)

    @command(is_error=True)
    def error(self, error):
        self.logger.warning(f'Update "{self.update}" caused error "{error}"')
        self.reply('An error occured, please try again later or contact the bot administrator')

    @command
    def start(self):
        self.logger.info(f'Start of user {self.user}')
        self.reply('Send me links to twitter users to get all their posted images')

    @command(handler=MessageHandler, filters=Filters.text)
    def do_something(self):
        text = self.message.text.replace('\n', ' ')
        self.logger.info(f'Do something {text}')

        self.message.reply_text(text)


me = updater.bot.get_me()
logger.info(f'Starting bot {me.name} {me.link}')
updater.start_polling()
updater.idle()
