# -*- coding: utf-8 -*-
import psycopg2
from flask import Flask, render_template

from photobagapp.model import db, calendar, comment, post, users, photo, group_photo

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app