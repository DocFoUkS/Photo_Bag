# -*- coding: utf-8 -*-

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import (current_user,
                         login_user, logout_user)

from photobagapp.db import db
from photobagapp.user.models import User
from photobagapp.user.forms import LoginForm, RegistrationForm

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    title = 'Авторизация'
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        login_form = LoginForm()
        return render_template('user/login.html',
                               page_title=title,
                               form=login_form)


@blueprint.route('/registration')
def registration():
    title = 'Регистрация'
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        registr_form = RegistrationForm()
        return render_template('user/registration.html',
                               page_title=title,
                               form=registr_form)


@blueprint.route('/process_login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(u'Добро пожаловать!')
            return redirect(url_for('main.index'))

    flash(u'Неправильный логин или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/process_registration', methods=['POST'])
def process_registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(u'Успешная регистрация')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash('Ошибка в поле {}: {}'.format(getattr(form, field).label.text, err))

        return redirect(url_for('user.registration'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash(u'Вы вышли из учетной записи')
    return redirect(url_for('main.index'))
