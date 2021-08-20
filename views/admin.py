from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_security import current_user
import subprocess
from config import APP_DIR


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        # Формируем Git Log
        format = '--format=format:<span class="git-version">%h</span>-' \
                 '<span class="git-time">(%ar)</span> %s - <b>%an</b>' \
                 '<span class="badge bg-warning text-dark">%d</span>'
        command = [
            'git',
            'log',
            '--graph',
            '--all',                # Все ветки
            format,
            '--abbrev-commit',      # Сокращенный номер коммита
            '--date=relative',
            '--since=6 month ago',  # Коммиты за последние 6 месяцев
        ]
        result = subprocess.run(command, cwd=APP_DIR, stdout=subprocess.PIPE)
        git_log = result.stdout.decode("utf-8")
        git_log = git_log.replace('\n', '<br />')

        return self.render('admin/index.html', git_log=git_log)


class PostAdminView(AdminMixin, ModelView):
    column_exclude_list = ['icon']


class UserAdminView(AdminMixin, ModelView):
    def _description_formatter(view, context, model, name):
        return model.password[:20]

    column_formatters = {
        'password': _description_formatter,
    }


class RoleAdminView(AdminMixin, ModelView):
    pass


class BirthdayAdminView(AdminMixin, ModelView):
    def _description_formatter(view, context, model, name):
        birthday = f'{str(model.birth_day).zfill(2)}.{str(model.birth_month).zfill(2)}.{model.birth_year}'
        return birthday

    column_formatters = {
        'birth_day': _description_formatter,
    }

    column_exclude_list = ['birth_month', 'birth_year']
