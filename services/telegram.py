import telebot
from config import Tokens


class TBot:
    """ Обёртка для работы с API Телеграм """
    def __init__(self):
        """ Инициализация бота """
        bot_token = Tokens.TELEGRAM_BOT_TOKEN
        self._bot = telebot.TeleBot(bot_token)

    def send_message(self, chat_id=-1001254598595, message=''):
        """ Отправка сообщения, chat_id - id группы или пользователя"""
        self._bot.send_message(chat_id, message)
