# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class calendar(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Calendar {} {}>'.format(self.event_id, self.user_id)
    

class comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)
    post_comment=db.relationship('post', backref='post_comment', lazy=True)
    photo_comment=db.relationship('photo', backref='photo_comment', lazy=True)
    gr_photo_comment=db.relationship('group_photo', backref='group_photo_comment', lazy=True)

    def __repr__(self):
        return '<Comment {} {}>'.format(self.comment_id, self.user_id)
    

class post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'), nullable=False)
    caption = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Post {} {}>'.format(self.post_id, self.caption)
    

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    town = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    telegram = db.Column(db.String, nullable=True)
    admin = db.Column(db.Integer, nullable=True)
    registration_date = db.Column(db.DateTime, nullable=True)
    calendar_user=db.relationship('calendar', backref='calendar_user', lazy=True)
    comment_user=db.relationship('comment', backref='comment_user', lazy=True)

    def __repr__(self):
        return '<Users {} {}>'.format(self.user_id, self.name)
    

class photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_photo.group_id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return '<Photo {} {}>'.format(self.photo_id, self.group_id)
    
    
class group_photo(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'), nullable=False)
    caption = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=True)
    photo_group=db.relationship('photo', backref='photo_group', lazy=True)

    def __repr__(self):
        return '<Group photo {} {}>'.format(self.group_id, self.caption)