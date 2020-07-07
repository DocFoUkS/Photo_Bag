# -*- coding: utf-8 -*-

import sys
from getpass import getpass
from datetime import datetime

from photobagapp import create_app
from photobagapp.db import db
from photobagapp.user.models import User

app = create_app()

with app.app_context():
    username = input(u'Введите имя пользователя для администратора: ')
    name = input(u'Введите имя администратора: ')
    email = input(u'Введите email администратора: ')
    town = input(u'Введите город администратора: ')
    phone = input(u'Введите телефон администратора: ')
    telegram = input(u'Введите Telegram администратора: ')
    registration_date = datetime.now().date()

    if User.query.filter(User.username == username).count():
        print(u'Уже существует такое имя пользователя')
        sys.exit(0)

    password = getpass(u'Введите пароль: ')
    password2 = getpass(u'Повторите введеный пароль: ')
    if not password == password2:
        print(u'Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, role='admin', name=name, email=email, town=town, phone=phone, telegram=telegram, registration_date=registration_date)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    print(u'Пользователь {user} создан с id {id}'.format(
                                                    user=new_user.username,
                                                    id=new_user.id))
