from flask import Flask
from flask import redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user
from config import Config


""" Flask App """
app = Flask(__name__)
app.config.from_object(Config)

""" База данных (DB). Для создания DB: from app import db + db.create_all() """
db = SQLAlchemy(app)
from models import *

""" Миграция ДБ
 For init command: flask db init
 For migration (after edit models in DB): flask db migrate + flask db upgrade"""
migrate = Migrate(app, db)


""" Администратор """
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))

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
