# -*- coding: utf-8 -*-

from photobagapp.db import db


class Photo(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    group_id = db.Column(db.Integer,
                         db.ForeignKey('group_photo.id'),
                         nullable=False)
    comment_id = db.Column(db.Integer,
                           db.ForeignKey('comment.id'),
                           nullable=False)
    data = db.Column(db.LargeBinary,
                     nullable=False)

    def __repr__(self):
        return '<Photo {} {}>'.format(self.photo_id, self.group_id)


class Group_photo(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    comment_id = db.Column(db.Integer,
                           db.ForeignKey('comment.id'),
                           nullable=False)
    caption = db.Column(db.String,
                        nullable=False)
    text = db.Column(db.Text,
                     nullable=True)
    photo_group = db.relationship('Photo',
                                  backref='Group_photo',
                                  lazy=True)

    def __repr__(self):
        return '<Group photo {} {}>'.format(self.group_id, self.caption)
