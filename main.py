import codecs
import os
import sys
import threading
import time
from datetime import datetime, timedelta

import telebot

from keyboards import *
from MOSGORSUD import search_mobile_arbitrazh_delo as arbitr
from MOSGORSUD import search_federal_sud as federal
from MOSGORSUD import search_mir_sud as mir
from SQL_work import mysq
from Subscriptions import run_subs as SUBS
from log_writer.writer import add_log

API_TOKEN = os.environ.get('token') if os.environ.get('token') else '884321214:AAEPCr7msVY8bnVkcFRXuzmVP1ELB1dTYRM'

bot = telebot.TeleBot(API_TOKEN)
bot.remove_webhook()

subscription = SUBS.read_subs()

dict_subs_rules = {
    0: {
        'FSSP_EGRUL': 10,
        'sud': 5,
        'subs': 2
    },
    1: {
        'FSSP_EGRUL': 30,
        'sud': 25,
        'subs': 20
    },
    2: {
        'FSSP_EGRUL': 50,
        'sud': 50,
        'subs': 45
    }
}

@bot.message_handler(content_types="text")
def handler_text(message):
    text = message.text.lower()
    texti = message.text
    idk = int(message.chat.id)
    u_name = message.chat.username or ''
    chel = mysq.Polzo(idk, u_name)
    text_mes(text, texti, idk, chel, message)


def text_mes(text, texti, idk, chel, message):
    global subscription
    if texti[0] == '/' and texti != '/start':
        # Блок отвечающий за команды админов
        admins(texti, idk, chel)
    elif idk < 0:
        return
    elif chel.step == 4000:
        return
    elif texti == "/start" or text == "главное менюℹ" or text == "↩️назад":
        # Блок отобраения начального сообщения с выбором запроса: ЕГРЮЛ, Суд рф, ФССП
        add_log('ID={}, отправил команду {}'.format(idk, texti))
        starting(idk, chel)
    elif (text == "1️⃣" and chel.step == 0 and (chel.egfam == '0' or chel.egreg == '0')) or (chel.step == 40 and text == 'новый поиск🔎'):
        # Блок для нового пользователя (введение ФИО или ИНН для запроса) при выборе 1. ЕГРЮЛ
        if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
            add_log('ID={}, делает новый запрос на ЕГРЮЛ'.format(idk))
            send_mes(idk, """Введите вашу фамилию, имя и отчество или ИНН""", chel.ban, keybez2)
            chel.set_step(10)
        else:
            add_log('ID={}, превышено количество запросов к ЕГРЮЛ по подписке'.format(idk))
            send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
            starting(idk, chel)
    elif text == "1️⃣" and chel.step == 0:
        if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
            # Блок с показом данных из БД по последнему запросу из ЕГРЮЛ ФИО пользователя/ИНН и регион
            add_log('ID={}, показ данных предыдущего запроса ЕГРЮЛ'.format(idk))
            send_mes(idk, f"""Ваши данные:
фамилия, имя и отчество или ИНН: {chel.egfam}
Ваш регион: {chel.egreg}
""", chel.ban, keynol)
            chel.set_step(40)
        else:
            add_log('ID={}, превышено количество запросов к ЕГРЮЛ по подписке'.format(idk))
            send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
            starting(idk, chel)
    elif chel.step == 40 and texti == 'Повторить поиск🔄':
        add_log('ID={}, отправил команду ЕГРЮЛ {}'.format(idk, texti))
        eg, nom = chel.egrul()
        markup3 = telebot.types.ReplyKeyboardMarkup(True, True)
        for i in range(1, nom+1):
            button = telebot.types.KeyboardButton('{}'.format(i))
            markup3.add(button)
        button = telebot.types.KeyboardButton('↩️Назад')
        markup3.add(button)
        try:
            send_mes(idk, eg, chel.ban, markup3)
        except Exception:
            send_mes(idk, 'Ничего не найдено⛔', chel.ban, keybez2)
        chel.set_step(12)
    elif chel.step == 10:
        add_log('ID={}, step {}'.format(idk, chel.step))
        chel.set_egrul_fam(texti)
        send_mes(idk, """Введите ваш регион цифрой, или -""", chel.ban, keybez2)
        chel.set_step(11)
    elif chel.step == 11:
        add_log('ID={}, step {}'.format(idk, chel.step))
        chel.set_egrul_reg(texti)
        eg, nom = chel.egrul()
        markup3 = telebot.types.ReplyKeyboardMarkup(True, True)
        for i in range(1, nom+1):
            button = telebot.types.KeyboardButton('{}'.format(i))
            markup3.add(button)
        button = telebot.types.KeyboardButton('↩️Назад')
        markup3.add(button)
        try:
            send_mes(idk, eg, chel.ban, markup3)
        except Exception:
            send_mes(idk, 'Ничего не найдено⛔', chel.ban, keybez2)
        chel.set_step(12)
    elif chel.step == 12:
        add_log('ID={}, step {}'.format(idk, chel.step))
        eg = chel.down_egrul(texti)
        send_doc(idk, eg, chel.ban)
        starting(idk, chel)
        chel.update_fssp_try(idk, chel.fssp_try + 1)
    elif (text == "3️⃣" and chel.step == 2000 and
          (chel.uid == '0' or chel.vhod == '0' or chel.nom == '0' or chel.stor == '0')) \
            or (chel.step == 110 and text == 'новый поиск🔎'):
        add_log('ID={}, первый поиск по Судам Москвы'.format(idk))
        send_mes(idk, """Введите Уникальный идентификатор дела или -""", chel.ban, keybez2)
        chel.set_step(100)
    elif (text == "2️⃣" and chel.step == 0) or (text == "1️⃣" and chel.step == 5201):
        add_log('ID={}, переход в поиск дел по судам'.format(idk))
        send_mes(
            idk,
            '''Выберите тип запроса:
"1️⃣" Поиск дел по федеральным судам общей юрисдикции
"2️⃣" Поиск дел по мировым судам
"3️⃣" Поиск по судам Москвы
"4️⃣" Поиск арбитражных дел''', chel.ban,
            keymenu_sud
        )
        if chel.step == 5201:
            SUBS.subs_mark = 1
        chel.set_step(2000)
    elif text == "5️⃣" and chel.step == 2000:
        add_log('ID={}, суды пункт - {}, step {}'.format(idk, texti, chel.step))
        send_mes(idk, 'Введите номер региона', chel.ban)     
        chel.set_step(2101)
    elif chel.step == 2101:
        add_log('ID={}, step {}'.format(idk, chel.step))
        federal.region = int(texti)
        send_mes(idk, 'Введите наименование суда (либо -)', chel.ban)
        chel.set_step(2102)
    elif chel.step == 2102:
        add_log('ID={}, step {}'.format(idk, chel.step))
        federal.sud_ish = texti
        send_mes(idk, 'Введите город, где располагается суд (либо -)', chel.ban)
        chel.set_step(2103)
    elif chel.step == 2103:
        add_log('ID={}, step {}'.format(idk, chel.step))
        federal.city_ish = texti
        if chel.fssp_try <= dict_subs_rules[chel.pay]['sud']:
            send_mes(idk, federal.search_federal_sud_contact(), chel.ban, keybez2)
            chel.update_sud_try(idk, chel.fssp_try + 1)
        else:
            add_log('ID={}, превышено количество запросов по судам по подписке'.format(idk))
            send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        starting(idk, chel)
    elif text == "2️⃣" and chel.step == 2000:
        add_log('ID={}, суды пункт - {}, step {}'.format(idk, texti, chel.step))
        send_mes(idk, 'Введите номер региона', chel.ban)
        chel.set_step(2301)
    elif chel.step == 2301:
        add_log('ID={}, step {}'.format(idk, chel.step))
        mir.region = int(texti)
        send_mes(idk, 'Введите наименование мирового суда либо его классификационный код', chel.ban)
        chel.set_step(2302)
    elif chel.step == 2302:
        add_log('ID={}, step {}'.format(idk, chel.step))
        mir.sud_name = texti
        send_mes(idk, 'Введите номер дела (формат 2-303/2012, где 2-303 - номер дела, 2012 - год регистрации)', chel.ban)
        chel.set_step(2303)
    elif chel.step == 2303:
        add_log('ID={}, step {}'.format(idk, chel.step))
        mir.delo_num = texti
        if SUBS.subs_mark == 1:
            send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
            subscription[str(idk)][mir.delo_num] = {
                'type': 'Мировой суд',
                'region': mir.region,
                'sud_name': mir.sud_name,
                'message':  mir.search_mir_delo()
            }
            send_mes(idk, 'Подписка на дело {} добавлена'.format(mir.delo_num), chel.ban)
            SUBS.subs_mark = 0
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
        else:
            if chel.fssp_try <= dict_subs_rules[chel.pay]['sud']:
                send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
                send_mes(idk, mir.search_mir_delo(), chel.ban, keybez2)
                chel.update_sud_try(idk, chel.fssp_try + 1)
            else:
                add_log('ID={}, превышено количество запросов по судам по подписке'.format(idk))
                send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        starting(idk, chel)
    elif text == "1️⃣" and chel.step == 2000:
        add_log('ID={}, суды пункт - {}, step {}'.format(idk, texti, chel.step))
        send_mes(idk, 'Введите номер региона', chel.ban)
        chel.set_step(2201)
    elif chel.step == 2201:
        add_log('ID={}, step {}'.format(idk, chel.step))
        federal.region = int(texti)
        send_mes(idk, 'Введите наименование суда', chel.ban)
        chel.set_step(2202)
    elif chel.step == 2202:
        add_log('ID={}, step {}'.format(idk, chel.step))
        federal.sud_fed_ish = texti
        send_mes(idk, 'Введите ФИО участника процесса (например, Иванов А.А. или -)', chel.ban)
        chel.set_step(2203)
    elif chel.step == 2203:
        add_log('ID={}, step {}'.format(idk, chel.step))
        federal.storona = texti
        send_mes(idk, 'Введите номер дела (например, 0-1234/2020)', chel.ban)
        chel.set_step(2204)
    elif chel.step == 2204:
        add_log('ID={}, step {}'.format(idk, chel.step))
        federal.delo_num = texti
        if SUBS.subs_mark == 1:
            send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
            subscription[str(idk)][federal.delo_num] = {
                'type': 'Федеральный суд общей юрисдикции',
                'region': federal.region,
                'sud_name': federal.sud_fed_ish,
                'storona': federal.storona,
                'message':  federal.search_federal_sud_delo()
            }
            send_mes(idk, 'Подписка на дело {} добавлена'.format(federal.delo_num), chel.ban)
            SUBS.subs_mark = 0
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
        else:
            if chel.fssp_try <= dict_subs_rules[chel.pay]['sud']:
                send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
                send_mes(idk, federal.search_federal_sud_delo(), chel.ban, keybez2)
                chel.update_sud_try(idk, chel.fssp_try + 1)
            else:
                add_log('ID={}, превышено количество запросов по судам по подписке'.format(idk))
                send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        starting(idk, chel)
    elif text == "4️⃣" and chel.step == 2000:
        add_log('ID={}, суды пункт - {}, step {}'.format(idk, texti, chel.step))
        send_mes(idk, 'Введите номер дела (например А00-12345/2020)', chel.ban)
        chel.set_step(2501)
    elif chel.step == 2501:
        add_log('ID={}, step {}'.format(idk, chel.step))
        arbitr.delo_num = texti
        if SUBS.subs_mark == 1:
            send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
            subscription[str(idk)][arbitr.delo_num] = {
                'type': 'Арбитражный суд',
                'message':  arbitr.search_arbitr_delo()
            }
            send_mes(idk, 'Подписка на дело {} добавлена'.format(arbitr.delo_num), chel.ban)
            SUBS.subs_mark = 0
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
        else:
            if chel.fssp_try <= dict_subs_rules[chel.pay]['sud']:
                send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
                send_mes(idk, arbitr.search_arbitr_delo(), chel.ban, keybez2)
                chel.update_sud_try(idk, chel.fssp_try + 1)
            else:
                add_log('ID={}, превышено количество запросов по судам по подписке'.format(idk))
                send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        starting(idk, chel)
    elif text == "3️⃣" and chel.step == 2000:
        add_log('ID={}, Суды Москвы показ предыдущего запроса'.format(idk))
        send_mes(idk, f"""Ваши данные:
Уникальный идентификатор дела {chel.uid}
Номер входящего документа {chel.vhod}
Номер дела, материала, жалобы или производства {chel.nom}
Стороны {chel.stor}
""", chel.ban, keynol)
        chel.set_step(110)
    elif chel.step == 100:
        add_log('ID={}, step {}'.format(idk, chel.step))
        chel.set_sudrf_uid(texti)
        send_mes(idk, """Номер входящего документа, или -""", chel.ban, keybez2)
        chel.set_step(101)
    elif chel.step == 101:
        add_log('ID={}, step {}'.format(idk, chel.step))
        chel.set_sudrf_vhod(texti)
        send_mes(idk, """Номер дела, материала, жалобы или производства, или -""", chel.ban, keybez2)
        chel.set_step(102)
    elif chel.step == 102:
        add_log('ID={}, step {}'.format(idk, chel.step))
        chel.set_sudrf_nom(texti)
        send_mes(idk, """Стороны, или -""", chel.ban, keybez2)
        chel.set_step(103)
    elif chel.step == 103:
        add_log('ID={}, step {}'.format(idk, chel.step))
        chel.set_sudrf_stor(texti)
        strok = chel.mosgor()
        if SUBS.subs_mark == 1:
            send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
            subscription[str(idk)][chel.nom] = {
                'type': 'МосГорСуд',
                'stor': chel.stor,
                'vhod': chel.vhod,
                'uid': chel.uid,
                'message':  strok
            }
            send_mes(idk, 'Подписка на дело {} добавлена'.format(chel.nom), chel.ban)
            SUBS.subs_mark = 0
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
            starting(idk, chel)
        else:
            if chel.fssp_try <= dict_subs_rules[chel.pay]['sud']:
                try:
                    send_mes(idk, strok, chel.ban, keybez2)
                except Exception:
                    send_mes(idk, "Не найдено⛔", chel.ban, keybez2)
                chel.update_sud_try(idk, chel.fssp_try + 1)
            else:
                add_log('ID={}, превышено количество запросов по судам по подписке'.format(idk))
                send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        chel.set_step(0)
    elif chel.step == 110 and texti == 'Повторить поиск🔄':
        add_log('ID={}, Повтор поиск, step {}'.format(idk, chel.step))
        strok = chel.mosgor()
        if chel.fssp_try <= dict_subs_rules[chel.pay]['sud']:
            try:
                send_mes(idk, strok, chel.ban, keybez2)
            except Exception:
                send_mes(idk, 'Ничего не найдено⛔', chel.ban, keybez2)
            chel.update_sud_try(idk, chel.fssp_try + 1)
        else:
            add_log('ID={}, превышено количество запросов по судам по подписке'.format(idk))
            send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        chel.set_step(0)
    elif (texti == "3️⃣" and chel.step == 0) or (texti == "2️⃣" and chel.step == 5201):
        add_log('ID={}, Поиск по ФССП'.format(idk))
        send_mes(idk, "Поиск физического, юридического лица или номер производства?", chel.ban, keyur)
        if chel.step == 5201:
            SUBS.subs_mark = 1
            chel.set_step(0)
    elif (text == "юридического" and chel.step == 0 and
          (str(chel.fsplegreg) == '0' or str(chel.name) == '0' or str(chel.address) == '0')) \
            or (chel.step == 210 and text == 'новый поиск🔎'):
        add_log('ID={}, ФССП первый поиск юридического лица или step {}'.format(idk, chel.step))
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        '''
        if time.time() - chel.timeog < chel.timeleg:
            send_mes(idk, f'Запрос неудачен⚠️ подождите ⏰{(chel.timeog-time.time()+chel.timeleg)//60} минут', keybez2)
            return
        '''
        send_mes(idk, """Введите Код региона отдела судебных приставов""", chel.ban, keybez2)
        chel.set_step(200)
    elif text == "юридического" and chel.step == 0:
        add_log('ID={}, ФССП поиск юридесчкого лица, показ предыдущего запроса'.format(idk))
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        '''
        if time.time() - chel.timeog < chel.timeleg:
            send_mes(idk, f'Запрос неудачен⚠️ подождите ⏰{(chel.timeog-time.time()+chel.timeleg)//60} минут', keybez2)
            return
        '''
        send_mes(idk, f"""Ваши данные:
Код региона отдела судебных приставов {chel.fsplegreg}
Фрагмент названия должника — юридического лица {chel.name}
Фрагмент юридического адреса юридического лица {chel.address}
""", chel.ban, keynol)
        chel.set_step(210)
    elif chel.step == 200:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fsppleg_reg(texti)
        send_mes(idk, """Фрагмент названия должника — юридического лица""", chel.ban, keybez2)
        chel.set_step(201)
    elif chel.step == 201:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fsppleg_name(texti)
        send_mes(idk, """Фрагмент юридического адреса юридического лица""", chel.ban, keybez2)
        chel.set_step(202)
    elif chel.step == 202:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fsppleg_address(texti)
        send_mes(idk,
                 f"{chel.fsspleg_zap()}, подождите некоторое время. Данные по запросу формируются.", chel.ban, keybez2)
        if SUBS.subs_mark == 1:
            subscription[str(idk)][chel.name] = {
                'type': 'ФССП. Поиск юр.лиц',
                'region': chel.fsplegreg,
                'ur_name': chel.name,
                'address': chel.address,
                'message':  chel.fssp_prov(1)
            }
            send_mes(idk, 'Подписка на {} добавлена'.format(chel.name), chel.ban)
            SUBS.subs_mark = 0
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
        else:
            if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
                send_mes(idk, chel.fssp_prov(1), chel.ban)
                chel.update_fssp_try(idk, chel.fssp_try + 1)
            else:
                add_log('ID={}, превышено количество запросов к ФССП по подписке'.format(idk))
                send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        starting(idk, chel)
    elif chel.step == 210 and texti == 'Повторить поиск🔄':
        add_log('ID={}, ФССП step {}, Повтор поиска'.format(idk, chel.step))
        send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        result = chel.fssp_prov(1, fssp_token)
        if not result:
            result = 'Информация не найдена, попробуйте изменить данные и сделать новый поиск'
        if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
            send_mes(idk, f"""{result}""", chel.ban, keybez2)
            chel.update_fssp_try(idk, chel.fssp_try + 1)
        else:
            add_log('ID={}, превышено количество запросов к ФССП по подписке'.format(idk))
            send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
    elif (text == "физического" and chel.step == 0 and
          (str(chel.fspreg) == '0' or str(chel.firstname) == '0' or str(chel.secondname) == '0' or str(chel.lastname) == '0' or str(chel.birthdate) == '0')) \
            or (chel.step == 310 and text == 'новый поиск🔎'):
        add_log('ID={}, ФССП первый поиск физического лица или step {}'.format(idk, chel.step))
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        '''
        if time.time() - chel.timeog < chel.timehys:
            send_mes(idk, f'Запрос неудачен⚠️ подождите ⏰{(chel.timeog-time.time()+chel.timehys)//60} минут', keybez2)
            return
        '''
        send_mes(idk, """Введите Код региона отдела судебных приставов""", chel.ban, keybez2)
        chel.set_step(300)
    elif text == "физического" and chel.step == 0:
        add_log('ID={}, ФССП поиск физических лиц, показ предыдущего запроса'.format(idk), chel.ban)
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        '''
        if time.time() - chel.timeog < chel.timehys:
            send_mes(idk, f'Запрос неудачен⚠️ подождите ⏰{(chel.timeog-time.time()+chel.timehys)//60} минут', keybez2)
            return
        '''
        send_mes(idk, f"""Ваши данные:
Код региона отдела судебных приставов {chel.fspreg}
Имя должника по исполнительному производству {chel.firstname}
Отчество должника по исполнительному производству {chel.secondname}
Фамилия должника по исполнительному производству {chel.lastname}
Дата рождения должника в формате «дд.мм.гггг» {chel.birthdate}
""", chel.ban, keynol)
        chel.set_step(310)
    elif chel.step == 300:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fspphys_reg(texti)
        send_mes(idk, """Имя должника по исполнительному производству""", chel.ban, keybez2)
        chel.set_step(301)
    elif chel.step == 301:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fspphys_firstname(texti)
        send_mes(idk, """Отчество должника по исполнительному производству""", chel.ban, keybez2)
        chel.set_step(302)
    elif chel.step == 302:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fspphys_secondname(texti)
        send_mes(idk, """Фамилия должника по исполнительному производству""", chel.ban, keybez2)
        chel.set_step(303)
    elif chel.step == 303:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fspphys_lastname(texti)
        send_mes(idk, """Дата рождения должника в формате «дд.мм.гггг»""", chel.ban, keybez2)
        chel.set_step(304)
    elif chel.step == 304:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fspphys_birthdate(texti)
        txt_zapros = chel.fssphys_zap()
        send_mes(
            idk,
            f"""{txt_zapros}, подождите некоторое время. Данные по запросу формируются.""",
            chel.ban,
            keybez2
        )
        if SUBS.subs_mark == 1:
            subscription[str(idk)]['{} {} {} {}'.format(chel.firstname, chel.secondname, chel.lastname, chel.birthdate)] = {
                'type': 'ФССП. Поиск физ.лиц',
                'region': chel.fspreg,
                'firstname': chel.firstname,
                'secondname': chel.secondname,
                'lastname': chel.lastname,
                'birthdate': chel.birthdate,
                'message':  chel.fssp_prov(0)
            }
            send_mes(idk, 'Подписка на {} {} {} добавлена'.format(chel.lastname, chel.firstname, chel.secondname), chel.ban)
            SUBS.subs_mark = 0
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
        else:
            if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
                send_mes(idk, chel.fssp_prov(0), chel.ban)
                chel.update_fssp_try(idk, chel.fssp_try + 1)
            else:
                add_log('ID={}, превышено количество запросов к ФССП по подписке'.format(idk))
                send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        starting(idk, chel)
    elif chel.step == 310 and texti == 'Повторить поиск🔄':
        add_log('ID={}, ФССП step {}, Повтор поиска'.format(idk, chel.step))
        send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        result = chel.fssp_prov(0, fssp_token)
        if not result:
            result = 'Информация не найдена, попробуйте изменить данные и сделать новый поиск'
        if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
            send_mes(idk, f"""{result}""", chel.ban, keybez2)
            chel.update_fssp_try(idk, chel.fssp_try + 1)
        else:
            add_log('ID={}, превышено количество запросов к ФССП по подписке'.format(idk))
            send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
            starting(idk, chel)
    ########################################
    elif (text == "производство"  and chel.step == 0 and (chel.numberip == 0 or chel.numberip == '0')) or(chel.step == 410 and text == 'новый поиск🔎'):
        add_log('ID={}, ФССП поиск исполнительного производства новый поиск или step {}'.format(idk, chel.step))
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        '''
        if time.time() - chel.timeog < chel.timeip:
            send_mes(idk, f'Запрос неудачен⚠️ подождите ⏰{(chel.timeog-time.time()+chel.timeip)//60} минут', keybez2)
            return
        '''
        send_mes(idk, """Введите Номер исполнительного производства в формате «n…n/yy/dd/rr» или «n…n/yy/ddddd-ИП», где:
n…n — собственная часть номера;
yy — последние две цифры года возбуждения ИП;
ddddd — полный номер отдела судебных приставов;
dd — последние две цифры номера отдела;
rr — номер региона отдела судебных приставов по справочнику регионов ФССП России""", chel.ban, keybez2)
        chel.set_step(400)
    elif chel.step == 400:
        add_log('ID={}, ФССП step {}'.format(idk, chel.step))
        chel.set_fsppip_number(texti)
        send_mes(idk,
                 f"""{chel.fsspip_zap()}, подождите некоторое время. Данные по запросу формируются.""", chel.ban, keybez2)
        if SUBS.subs_mark == 1:
            subscription[str(idk)][chel.numberip] = {
                'type': 'ФССП. Поиск исполнительного производства',
                'numberip': chel.numberip,
                'message':  chel.fssp_prov(2)
            }
            send_mes(idk, 'Подписка на {} добавлена'.format(chel.name), chel.ban)
            SUBS.subs_mark = 0
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
        else:
            if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
                send_mes(idk, chel.fssp_prov(2), chel.ban)
                chel.update_fssp_try(idk, chel.fssp_try + 1)
            else:
                add_log('ID={}, превышено количество запросов к ФССП по подписке'.format(idk))
                send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
        starting(idk, chel)
    elif text == "производство" and chel.step == 0:
        add_log('ID={}, ФССП поиск исполнительного производства, показ предыдущего запроса'.format(idk, chel.step))
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        '''
        if time.time() - chel.timeog < chel.timeip:
            send_mes(idk, f'Запрос неудачен⚠️ подождите ⏰{(chel.timeog-time.time()+chel.timeip)//60} минут', keybez2)
            return
        '''
        send_mes(idk, f"""Ваши данные:
Номер исполнительного производства:{chel.numberip}
""", chel.ban, keynol)
        chel.set_step(410)
    elif chel.step == 410 and text == 'Повторить поиск🔄':
        add_log('ID={}, ФССП step {}, Повтор поиска'.format(idk, chel.step))
        send_mes(idk, 'Пожалуйста подождите. Запрос обрабатывается.', chel.ban)
        time_wait, fssp_token = chel.fssp_time_count()
        if time_wait > 0:
            send_mes(idk, '⚠️ Система занята. Пожалуйста, подождите {} секунд'.format(time_wait), chel.ban, keybez2)
            return
        result = chel.fssp_prov(2, fssp_token)
        if not result:
            result = 'Информация не найдена, попробуйте изменить данные и сделать новый поиск'
        if chel.fssp_try <= dict_subs_rules[chel.pay]['FSSP_EGRUL']:
            send_mes(idk, f"{result}", chel.ban, keybez2)
            chel.update_fssp_try(idk, chel.fssp_try + 1)
        else:
            add_log('ID={}, превышено количество запросов к ФССП по подписке'.format(idk))
            send_mes(idk, """Превышено количество запросов в день по подписке.""", chel.ban)
            starting(idk, chel)
    elif text == "4️⃣" and chel.step == 0:
        add_log('ID={}, перешел в подписки'.format(idk))
        send_mes(idk, 'Выберите пункт меню для продолжения', chel.ban, keysubs)
        chel.set_step(5000)
    elif chel.step == 5000 and texti == '🗓Список подписок':
        add_log('ID={}, Подписки step {}, Просмотр списка подписок'.format(idk, chel.step))
        send_mes(idk, 'Список доступных подписок:\n{}'.format(SUBS.view_subs(subscription, idk)), chel.ban, keybez2)
    elif chel.step == 5000 and texti == '❌Убрать подписки':
        add_log('ID={}, Подписки step {}, Удаление подписки'.format(idk, chel.step))
        send_mes(idk, 'Введите номер дела', chel.ban, keybez2)
        chel.set_step(5101)
    elif chel.step == 5101:
        add_log('ID={}, Подписки step {}, Удаление дела из подписок'.format(idk, chel.step))
        SUBS.delo = texti
        SUBS.del_subs(subscription, str(idk))
        send_mes(idk, 'Дело {} успешно удалено из подписок'.format(texti), chel.ban)
        starting(idk, chel)
    elif chel.step == 5000 and texti == '📥Добавить подписки':
        if len(subscription[str(idk)]) <= dict_subs_rules[chel.pay]['subs']:
            add_log('ID={}, Подписки step {}, Добавление подписки'.format(idk, chel.step))
            if str(idk) not in subscription:
                subscription[str(idk)] = {}
            send_mes(
                idk,
                '''Выберите сервис для подписки:
    "1️⃣" - Суды ⚖️
    "2️⃣" -  ФССП 💰''', chel.ban,
                keymenu_subs_service
            )
            chel.set_step(5201)
        else:
            add_log('ID={}, превышено количество уведомлений по подписке'.format(idk))
            send_mes(idk, """Превышено количество уведомлений по подписке.""", chel.ban)
            starting(idk, chel)
    elif chel.step == 5000 and texti == '🔄Обновить статус':
        add_log('ID={}, Подписки step {}, Обновление списка подписок'.format(idk, chel.step))
        send_mes(idk, 'Статус подписок обновляется. Пожалуйста подождите', chel.ban)
        old_subs = subscription
        for id_user in list(subscription.keys()):
            if str(idk) == id_user:
                if subscription[id_user] != {}:
                    old_subs = subscription[id_user]
                    for delo_num in list(subscription[id_user].keys()):
                        print(delo_num)
                        subscription[id_user][delo_num]['message'] = diff_subs(subscription[id_user][delo_num], id_user, delo_num)
                    new_subs = subscription[id_user]
                    if old_subs == new_subs:
                        send_mes(idk, 'Изменений не нашлось', chel.ban)
        SUBS.write_subs(subscription)
        subscription = SUBS.read_subs()
        send_mes(idk, 'Список подписок обновлен', chel.ban, keybez2)
        starting(idk, chel)
    else:
        add_log('ID={}, Я не понял вашей команды🤖'.format(idk))
        # если пользователь ввёл что то не по сценарию
        send_mes(idk, "Я не понял вашей команды🤖", chel.ban, 5)


def send_mes(idk, text, ban=0, key=telebot.types.ReplyKeyboardRemove()):
    if key == 5:
        key = ""
    if idk < 0:
        key = telebot.types.ReplyKeyboardRemove()
    try:
        if ban == 0:
            bot.send_message(chat_id=idk, text=text,reply_markup = key)
    except telebot.apihelper.ApiException:
        add_log('Не получилось отправить сообщение пользователю {}'.format(idk))


def send_doc(idk, text, ban):
    if ban == 0:
        with open(text, 'rb') as f:
            bot.send_document(idk, f, 'выписка', 'выписка')
        #path = os.path.join(os.path.abspath(os.path.dirname(__file__)), text)
        os.remove(text)


def starting(idk, chel):
    send_mes(idk, """Выберите сервис, нажмите кнопку
"1️⃣" - Реестры ЕГРЮЛ/ЕГРИП 📚
"2️⃣" - Суды ⚖️
"3️⃣" - ФССП 💰
"4️⃣" - Подписки 🗓""", key=keymenu)
    chel.set_step(0)


def admins(texti, idk, chel):
    if texti == "/setpravadminov":
        chel.set_step(1000)
        send_mes(idk, """Вы теперь обладаете правами админа.""", chel.ban)
    elif texti == "/ubrpravadminov":
        chel.set_step(0)
        send_mes(idk, """У вас больше нет прав.""", chel.ban, keymenu)
    elif texti[:5] == "/soed" and chel[4] == 1000:
        nomer = texti.split()[1]
        chel.set_adm(nomer, idk)
        send_mes(idk, """Ваш чат соединен с {}""".format(nomer), chel.ban)
    elif texti[:5] == "/raze" and chel[4] == 1000:
        nomer = texti.split()[1]
        chel.ub_adm(nomer, idk)
        send_mes(idk, """Ваш чат разъединен с {}""".format(nomer), chel.ban)
        send_mes(int(nomer), """Главное меню""", chel.ban, keymenu)
    elif texti[:8] == '/add_ban' and chel.admin > 0 and len(texti.split(' ')) == 2:
        ban_person = texti.split(' ')[1]
        chel.add_ban(ban_person)
        send_mes(idk, 'Бан пользователю {} выдан'.format(ban_person), chel.ban)
        add_log('Бан пользователю {} выдан. Выдал {}'.format(ban_person, idk))
        starting(idk, chel)
    elif texti[:7] == '/rm_ban' and chel.admin > 0 and len(texti.split(' ')) == 2:
        ban_person = texti.split(' ')[1]
        chel.rm_ban(ban_person)
        send_mes(idk, 'Бан пользователю {} снят'.format(ban_person), chel.ban)
        add_log('Бан пользователю {} снят. Выдал {}'.format(ban_person, idk))
        starting(idk, chel)
    elif texti[:9] == '/list_ban' and chel.admin > 0:
        send_mes(idk, 'Список забаненных пользователей:\n{}'.format(chel.list_ban()), chel.ban)
        add_log('{} посмотрел список забаненных пользователей'.format(idk))
        starting(idk, chel)
    elif texti[:10] == '/add_admin' and chel.admin > 0 and len(texti.split(' ')) == 2:
        admin_person = texti.split(' ')[1]
        chel.add_admin(admin_person)
        send_mes(idk, 'Пользователь {} стал админом'.format(admin_person), chel.ban)
        add_log('Пользователь {} стал админом. Выдал {}'.format(admin_person, idk))
        starting(idk, chel)
    elif texti[:9] == '/rm_admin' and chel.admin > 0 and len(texti.split(' ')) == 2:
        admin_person = texti.split(' ')[1]
        chel.rm_admin(admin_person)
        send_mes(idk, 'Пользователь {} потерял права админа'.format(admin_person), chel.ban)
        add_log('Пользователь {} потерял права админа. Выдал {}'.format(admin_person, idk), chel.ban)
        starting(idk, chel)
    elif texti[:11] == '/list_admin' and chel.admin > 0:
        send_mes(idk, 'Список админов\n{}'.format(chel.list_admin()), chel.ban)
        add_log('{} посмотрел список админов'.format(idk))
        starting(idk, chel)
    elif texti[:15] == '/list_free_user' and chel.admin > 0:
        send_mes(idk, 'Список пользователей без подписки:\n{}'.format(chel.list_free_user()), chel.ban)
        add_log('{} посмотрел список пользователей без подписки'.format(idk))
        starting(idk, chel)
    elif texti[:15] == '/list_pay_user' and chel.admin > 0:
        send_mes(idk, 'Список пользователей c подпиской:\n{}'.format(chel.list_pay_user()), chel.ban)
        add_log('{} посмотрел список пользователей с подпиской'.format(idk))
        starting(idk, chel)
    elif texti[:10] == '/last_week' and chel.admin > 0:
        send_mes(idk, 'Список пользователей с неделей до конца подписки:\n{}'.format(chel.list_last_week()), chel.ban)
        add_log('{} посмотрел список пользователей с неделей до конца подписки'.format(idk))
        starting(idk, chel)
    elif texti[:5] == '/help' and chel.admin > 0:
        send_mes(idk, '''Список комманд:\n
/add_ban <id пользователя> - отправить пользователя в бан
/rm_ban <id пользователя> - снять бан с пользователя
/list_ban - список забаненных пользователей
/add_admin <id пользователя> - добавить админа
/rm_admin <id пользователя> - убрать админа
/list_admin - список админов
/list_free_user - список пользователей без подписки
/list_pay_user - список пользователей с подписками (разделяются по типу подписки)
/last_week - список пользователей, у которых заканчивается последняя неделя подписки, либо она закончилась
/help - список комманд
/start - открыть меню бота''', chel.ban)
        add_log('{} посмотрел список команд'.format(idk))
        starting(idk, chel)
    elif texti[:5] == '/help' and chel.admin == 0:
        send_mes(idk, '''Список комманд:\n
/start - открыть меню бота
/want_admin - отправить запрос на добавление админских прав''', chel.ban)
        add_log('{} посмотрел список команд'.format(idk))
        starting(idk, chel)
    elif texti[:11] == '/want_admin' and chel.admin == 0:
        for admin_user in chel.list_admin_message():
            print(admin_user)
            send_mes(admin_user, 'Пользователь @{} хочет стать админом. Его ID: {}'.format(chel.u_name, idk))
        add_log('{} хочет стать админом'.format(idk))
        starting(idk, chel)


def bot_polling_start():
    while True:
        try:
            bot.polling(none_stop=False)
        except Exception as err:
            sys.stderr.write("TELEGRAMBOT ERROR: " + str(err) + "\n")
            time.sleep(3)
            sys.stderr.write("TELEGRAMBOT RESTART\n")


def diff_subs(delo_dict, id_user, delo_num):
    chel = mysq.Polzo(id_user, id_user)
    if delo_dict['type'] == 'Мировой суд':
        mir.region = delo_dict['region']
        mir.sud_name = delo_dict['sud_name']
        mir.delo_num = 'delo_num'
        message_new = mir.search_mir_delo()
    
    if delo_dict['type'] == 'Федеральный суд общей юрисдикции':
        federal.region = delo_dict['region']
        federal.sud_fed_ish = delo_dict['sud_name']
        federal.storona = delo_dict['storona']
        federal.delo_num = delo_num
        message_new = federal.search_federal_sud_delo()
    
    if delo_dict['type'] == 'Арбитражный суд':
        arbitr.delo_num = delo_num
        message_new = arbitr.search_arbitr_delo()
    
    if delo_dict['type'] == 'МосГорСуд':
        chel.nom = delo_num
        chel.stor = delo_dict['stor']
        chel.vhod = delo_dict['vhod']
        chel.uid = delo_dict['uid']
        message_new = chel.mosgor()
    
    if delo_dict['type'] == 'ФССП. Поиск юр.лиц':
        chel.name = delo_num
        chel.fsplegreg = delo_dict['region']
        chel.address = delo_dict['address']
        chel.fsspleg_zap()
        message_new = chel.fssp_prov(1)
    
    if delo_dict['type'] == 'ФССП. Поиск физ.лиц':
        chel.fspreg = delo_dict['region']
        chel.firstname = delo_dict['firstname']
        chel.secondname = delo_dict['secondname']
        chel.lastname = delo_dict['lastname']
        chel.birthdate = delo_dict['birthdate']
        chel.fssphys_zap()
        message_new = chel.fssp_prov(0)
    
    if delo_dict['type'] == 'ФССП. Поиск исполнительного производства':
        chel.numberip = delo_dict['numberip']
        chel.fsspip_zap()
        message_new = chel.fssp_prov(2)
    
    if delo_dict['message'] != message_new:
        send_mes(int(id_user), '⚠️Обновилась информация по {}, дело {}:\n{}'.format(delo_dict['type'], delo_num, message_new))
        starting(int(id_user), chel)
        add_log('ID {}, обновилась информация по {}, дело {}'.format(id_user, delo_dict['type'], delo_num))
        return message_new
    return delo_dict['message']        


def clear_tries():
    add_log('Обнуление количества запросов')
    chel = mysq.Polzo(769386353, 'EAAgency')
    chel.update_day_try()
    add_log('Обнуление количества запросов завершено')


def clear_cookies():
    add_log('Чистка cookie')
    cookie_dir = r'C:\lawer_bot\selenium_driver\cache2\entries'
    stamptime = datetime.now().timestamp()
    for el in os.listdir(cookie_dir):
        if os.stat(cookie_dir + '\\' + el).st_atime < stamptime - 60*6:
            os.remove(cookie_dir + '\\' + el)


if __name__ == "__main__":
    # Запуск всего
    threading.Thread(target=bot_polling_start).start()
    mark_subs = 0
    mark_refresh = 0
    mark_minute = 0
    while True:
        if datetime.now().minute in (0, 1, 2, 30, 31, 32) and mark_minute == 0:
            clear_cookies()
            mark_minute = 1
        elif datetime.now().minute not in (0, 1, 2, 30, 31, 32):
            mark_minute = 0
        if datetime.now().hour == 0 and mark_refresh == 0:
            clear_tries()
            mark_refresh = 1
        if datetime.now().hour in (0, 12) and mark_subs == 0:
            print('Поиск обновлений подписок')
            add_log('Поиск обновлений подписок')
            for id_user in list(subscription.keys()):
                if subscription[id_user] != {}:
                    for delo_num in list(subscription[id_user].keys()):
                        subscription[id_user][delo_num]['message'] = diff_subs(subscription[id_user][delo_num], id_user, delo_num)
            SUBS.write_subs(subscription)
            subscription = SUBS.read_subs()
            mark_subs = 1
        if datetime.now().hour in (1, 13):
            mark_subs = 0
            mark_refresh = 0
        time.sleep(60*20)