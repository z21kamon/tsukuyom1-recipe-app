from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort
from flask_admin import AdminIndexView


class CustomIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

    def is_visible(self):
        return current_user.is_authenticated and current_user.id == 1

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

    def is_visible(self):
        return current_user.is_authenticated and current_user.id == 1

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)
