# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, TextAreaField, TimeField
from wtforms.validators import ValidationError

from photobagapp.calendar.models import Calendar


class PhotoSessionForm(FlaskForm):
    datesession = DateField('Дата фотосессии',
                            render_kw={'class': 'form-control'})
    sessiontime = TimeField('Длительность фотосессии',
                            render_kw={'class': 'form-control'})
    textsession = TextAreaField('Коментарий к фотосессии',
                                render_kw={'class': 'form-control'})
    submit = SubmitField('Записаться',
                         render_kw={'class': 'btn btn-primary'})

    def validate_datesession(self, datesession):
        session_count = Calendar.query.filter_by(date_time=datesession.data).count()
        if session_count > 0:
            raise ValidationError(u'Эта дата занята. Выберите, пожалуйста, другую')
