import os

from dotenv import load_dotenv


load_dotenv()

DEBUG = os.getenv('FLASK_DEBUG')
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
FLASK_DIR = os.getenv('FLASK_FOLDER')
# Debug включен на только локальном сервере, на сервере немного другой путь
if DEBUG == 0:
    BASE_DIR = os.path.join(BASE_DIR, FLASK_DIR)


class Config:
    DEBUG = DEBUG
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'


class Tokens:
    TINKOFF_SECRET_KEY = os.getenv('TINKOFF_SECRET_KEY')
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


class Vars:
    # Налоговый вычет ИИС
    TINKOFF_TAX_PLUS = os.getenv('TINKOFF_TAX_PLUS')
    # Временная зона
    TIME_ZONE = 'Europe/Moscow'
