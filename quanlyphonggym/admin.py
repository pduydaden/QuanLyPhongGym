from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme

from models import User, GoiTap, HoaDon
from quanlyphonggym import app, db

admin = Admin(app=app, name="TDGym", theme=Bootstrap4Theme())

admin.add_view(ModelView(GoiTap, db.session))
admin.add_view(ModelView(User, db.session))