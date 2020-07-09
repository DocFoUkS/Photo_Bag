# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, flash, url_for, render_template
from flask_login import current_user

from photobagapp.calendar.forms import PhotoSessionForm
from photobagapp.calendar.models import Calendar
from photobagapp.user.models import User
from photobagapp.db import db

blueprint = Blueprint('calendar', __name__)


@blueprint.route('/calendar')
def calendar():
    title = 'Запись на фотосессию'
    login_form = PhotoSessionForm()
    return render_template('calendar/calendar.html',
                           page_title=title,
                           form=login_form)


@blueprint.route('/process_event', methods=['POST'])
def process_event():
    form = PhotoSessionForm()

    if form.validate_on_submit():
        new_event = Calendar(user_id=User.query.filter_by(username=current_user.username).id,
                             date_time=form.datesession.data,
                             event_time=form.sessiontime.data,
                             text=form.textsession.data)
        new_event.set_password(form.password.data)
        db.session.add(new_event)
        db.session.commit()
        flash(u'Успешная запись на фотосессию')
        return redirect(url_for('main.index'))
    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash('Ошибка в поле {}: {}'.format(getattr(form, field).label.text, err))

        return redirect(url_for('calendar.calendar'))