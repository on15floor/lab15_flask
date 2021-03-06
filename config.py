import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('FLASK_DEBUG')

# Директории
DB_DIR = os.path.dirname(os.path.abspath(__name__))
APP_DIR = DB_DIR
SRV_DIR = os.getenv('FLASK_FOLDER')
if DEBUG == '0':    # Debug включен только на локальном сервере, на боевом сервере немного другой путь
    APP_DIR = os.path.join(APP_DIR, SRV_DIR)

# Базы данных
MONGO_CONN_STRING = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}" \
                    f"@cluster0.f5t4t.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


class Config:
    DEBUG = DEBUG
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'


class Tokens:
    FLASK_API_TOKEN = os.getenv('FLASK_API_TOKEN')
    TINKOFF_SECRET_KEY = os.getenv('TINKOFF_SECRET_KEY')
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


class Vars:
    # Налоговый вычет ИИС
    TINKOFF_TAX_PLUS = os.getenv('TINKOFF_TAX_PLUS')
    # Временная зона
    TIME_ZONE = 'Europe/Moscow'
