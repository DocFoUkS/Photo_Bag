# -*- coding: utf-8 -*-

from photobagapp.db import db


class Comment(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    date_time = db.Column(db.DateTime,
                          nullable=False)
    text = db.Column(db.Text,
                     nullable=True)
    post_comment = db.relationship('Blog',
                                   backref='post_comment',
                                   lazy=True)
    photo_comment = db.relationship('Photo',
                                    backref='photo_comment',
                                    lazy=True)
    gr_photo_comment = db.relationship('Group_photo',
                                       backref='Group_photo_comment',
                                       lazy=True)

    def __repr__(self):
        return '<Comment {} {}>'.format(self.comment_id, self.user_id)
