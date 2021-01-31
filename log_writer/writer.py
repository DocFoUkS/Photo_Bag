# -*- coding: utf-8 -*-

import codecs
import os
from datetime import datetime, timedelta


def add_log(text_line):
    for log_el in os.listdir(r'C:\Telegram_bot\logs'):
        if log_el == 'log-{}.txt'.format(str(datetime.now() - timedelta(days=7)).split(' ')[0]):
            os.remove(r'C:\Telegram_bot\logs/{}'.format(log_el))
    with codecs.open(r'C:\Telegram_bot\logs/log-{}.txt'.format(datetime.now().date()), 'a', encoding='utf-8') as filewrite:
        filewrite.write('{time} - {text}\n'.format(time=datetime.now(), text=text_line))
        print('{time} - {text}'.format(time=datetime.now(), text=text_line))
