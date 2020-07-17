# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, flash, url_for, render_template
from flask_login import current_user

from photobagapp.calendar.forms import PhotoSessionForm
from photobagapp.calendar.models import Calendar
from photobagapp.user.models import User
from photobagapp.db import db
from telegram_bot import bot as BT

blueprint = Blueprint('calendar', __name__)


def photosession_msg(date_session, long_session, comment_session):
    bot = BT.Telegram_BOT()
    admin_chat_id = '{}'.format(User.query.filter_by(role='admin').first().telegram)
    user_info = User.query.filter_by(id=current_user.id).first()
    session_text = '''Пользователь @{user} записался на фотосессию.
    Дата: {date}
    Продолжительность: {long}
    Комментарий: {comment}'''.format(
        user=user_info.telegram,
        date=date_session,
        long=long_session,
        comment=comment_session)
    message = {
        'chat_id': admin_chat_id,
        'text': session_text
    }
    bot.send_message(message=message)


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
        new_event = Calendar(user_id=current_user.id,
                             date_time=form.datesession.data.strftime('%d.%m.%Y') + ' ' + form.timesession.data.strftime('%H:%M'),
                             event_time=form.session.data.strftime('%H:%M'),
                             text=form.textsession.data)
        db.session.add(new_event)
        db.session.commit()
        flash(u'Успешная запись на фотосессию')
        photosession_msg(form.datesession.data.strftime('%d.%m.%Y') + ' ' + form.timesession.data.strftime('%H:%M'),
                         form.session.data.strftime('%H:%M'),
                         form.textsession.data)
        return redirect(url_for('main.index'))
    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash('Ошибка в поле {}: {}'.format(getattr(form, field).label.text, err))

        return redirect(url_for('calendar.calendar'))
