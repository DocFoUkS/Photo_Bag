# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import ValidationError
from wtforms.fields.html5 import DateField, TimeField

from photobagapp.calendar.models import Calendar


class PhotoSessionForm(FlaskForm):
    datesession = DateField('Дата фотосессии',
                            format='%Y-%m-%d',
                            render_kw={'class': 'form-control',
                                       'type': "date",
                                       'placeholder': "date naissance"})
    timesession = TimeField('Время фотосессии',
                            format='%H:%M',
                            render_kw={'class': 'form-control',
                                       'type': "time",
                                       'placeholder': "time naissance"})
    session = TimeField('Время фотосессии',
                            format='%H:%M',
                            render_kw={'class': 'form-control',
                                       'type': "time",
                                       'placeholder': "time naissance"})
    textsession = TextAreaField('Коментарий к фотосессии',
                                render_kw={'class': 'form-control'})
    submit = SubmitField('Записаться',
                         render_kw={'class': 'btn btn-primary'})

    def validate_datesession_timesession_session(self, datesession, timesession, session):
        session_count = Calendar.query.filter(Calendar.date_time >= datesession.data.strftime('%Y-%m-%d') + ' '+timesession.data.strftime('%H:%M'), Calendar.date_time <= datesession.data.strftime('%Y-%m-%d') + ' '+(timesession.data + session.data).strftime('%H:%M')).count()
        if session_count > 0:
            raise ValidationError(u'Эта дата занята. Выберите, пожалуйста, другую')
