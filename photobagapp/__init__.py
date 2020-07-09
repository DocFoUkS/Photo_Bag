# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from photobagapp.admin.views import blueprint as admin_blueprint
from photobagapp.blog.models import Blog
from photobagapp.blog.views import blueprint as blog_blueprint
from photobagapp.calendar.models import Calendar
from photobagapp.calendar.views import blueprint as calendar_blueprint
from photobagapp.comment.models import Comment
from photobagapp.db import db
from photobagapp.main.views import blueprint as main_blueprint
from photobagapp.portfolio.models import Group_photo, Photo
from photobagapp.portfolio.views import blueprint as portfolio_blueprint
from photobagapp.user.models import User
from photobagapp.user.views import blueprint as user_blueprint


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
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(calendar_blueprint)
    app.register_blueprint(portfolio_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
