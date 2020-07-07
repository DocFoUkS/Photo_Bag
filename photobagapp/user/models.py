# -*- coding: utf-8 -*-

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from photobagapp.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), index=True)
    town = db.Column(db.String, index=True)
    phone = db.Column(db.String, index=True)
    telegram = db.Column(db.String, index=True)
    role = db.Column(db.String(10), index=True)
    registration_date = db.Column(db.DateTime, nullable=True)
    calendar_user = db.relationship('Calendar', backref='calendar_user',
                                    lazy=True)
    comment_user = db.relationship('Comment', backref='comment_user',
                                   lazy=True)

    def __repr__(self):
        return '<User {}>'.fromat(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'
