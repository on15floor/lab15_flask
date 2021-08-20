from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

from config import Config

""" Flask App """
app = Flask(__name__)
app.config.from_object(Config)

""" Логирование ошибок """
if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('errors.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

""" База данных (DB). Для создания DB: from app import db + db.create_all() """
db = SQLAlchemy(app)
if db:
    from models import *
    from views import *
    from utils.filters import *

""" Миграция ДБ
 For init command: flask db init
 For migration (after edit models in DB): flask db migrate + flask db upgrade"""
migrate = Migrate(app, db)

""" Администратор """
admin = Admin(app, 'Lab15', url='/', index_view=HomeAdminView(), template_mode='bootstrap4')
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_view(BirthdayAdminView(Birthday, db.session))

""" Flask-Security 
 Добавление первого пользователя: 
 from app import db, user_datastore
 user = user_datastore.create_user(email='email@email.com', password='password')
 db.session.add(user), db.session.commit()
 Добавление первой роли:
 role = user_datastore.create_role(name='Admin')
 db.session.add(role), db.session.commit()
 Добавление роли к пользователю:
 user_datastore.add_role_to_user(user, role), db.session.commit() """
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
