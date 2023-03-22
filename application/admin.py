from flask import redirect, url_for
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

class MyAdminViewMixin():
    """Contains a method for admin authentication and a callback if auth. fails"""
    def is_accessible(self):
        if current_user and hasattr(current_user, 'role') and current_user.role.name == 'Admin':
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home.index'))

class MyAdminIndexView(MyAdminViewMixin, AdminIndexView):
    """ Class that manages access to /admin page """
    pass

class MyModelView(MyAdminViewMixin, ModelView):
    """ Class that manages access to /admin/<view> pages"""
    pass


class MyAdmin():

    def __init__(self) -> None:
        pass

    def init_admin(self, app, db) -> None:
        from application.models.model import Post, Tag, Role, User
        self.admin = Admin(app, index_view=MyAdminIndexView())
        self.admin.add_view(MyModelView(Post, db.session))
        self.admin.add_view(MyModelView(Tag, db.session))
        self.admin.add_view(MyModelView(User, db.session))
        self.admin.add_view(MyModelView(Role, db.session))
