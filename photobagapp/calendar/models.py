# -*- coding: utf-8 -*-

from photobagapp.db import db


class Calendar(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    date_time = db.Column(db.DateTime,
                          nullable=False)
    event_time = db.Column(db.Time,
                           nullable=False)
    text = db.Column(db.Text,
                     nullable=True)

    def __repr__(self):
        return '<Calendar {} {}>'.format(self.event_id, self.user_id)
