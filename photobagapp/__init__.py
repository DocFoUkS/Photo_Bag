# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate

from flask_login import LoginManager
from photobagapp.admin.views import blueprint as admin_blueprint
from photobagapp.db import db
from photobagapp.user.models import User
from photobagapp.user.views import blueprint as user_blueprint
from photobagapp.blog.models import Blog
from photobagapp.calendar.models import Calendar
from photobagapp.comment.models import Comment
from photobagapp.portfolio.models import Photo, Group_photo
from photobagapp.main.views import blueprint as main_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(main_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
