# -*- coding: utf-8 -*-

from photobagapp.db import db


class Blog(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    photo_id = db.Column(db.Integer,
                         db.ForeignKey('photo.id'),
                         nullable=False)
    comment_id = db.Column(db.Integer,
                           db.ForeignKey('comment.id'),
                           nullable=False)
    caption = db.Column(db.String,
                        nullable=False)
    date_time = db.Column(db.DateTime,
                          nullable=False)
    text = db.Column(db.Text,
                     nullable=True)

    def __repr__(self):
        return '<Blog {} {}>'.format(self.post_id, self.caption)
