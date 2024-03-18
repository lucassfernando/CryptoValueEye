import os

import telebot
from dotenv import load_dotenv


class BotTelegram:

    def __init__(self, token_api=None):
        if token_api:
            self.token_api = token_api

        else:
            load_dotenv()
            self.token_api = os.getenv('TELEGRAM_TOKEN')
        self.bot = telebot.TeleBot(self.token_api)       

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)
    