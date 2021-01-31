# -*- coding: utf-8 -*-

import codecs
import json


delo = ''
subs_mark = 0


def read_subs():
    '''
    Read Subscriptions from Subscriptions\Subscriptions.json
    '''
    with codecs.open(r'C:\Telegram_bot\Subscriptions\Subscriptions.json', 'r', encoding='utf-8') as subs_read:
        return json.load(subs_read)


def write_subs(dist_sub):
    '''
    Write new dict of substrictions in Subscriptions\Subscriptions.json
    '''
    with codecs.open(r'C:\Telegram_bot\Subscriptions\Subscriptions.json', 'w', encoding='utf-8') as subs_read:
        json.dump(
            dist_sub,
            subs_read,
            indent=4,
            sort_keys=True,
            separators=(',', ': '),
            ensure_ascii=False
        )


def diff_substrictions(subs, new_subs):
    dict_answer = {}
    for id_user in list(new_subs.keys()):
        for delo_num in list(new_subs[id_user].keys()):
            if new_subs[id_user][delo_num]['message'] != subs[id_user][delo_num]['message']:
                dict_answer.setdefault(id_user, {'message': ''})['message'] += u'Появились новые сведения по делу {} ({}):{}'.format(
                    delo_num,
                    new_subs[id_user][delo_num]['type'],
                    subs[id_user][delo_num]['message']
                )


def view_subs(subs, id_user):
    answer_str = ''
    dict_delo = {}
    for id_usr in list(subs.keys()):
        if id_usr == str(id_user):
            for delo_num in list(subs[id_usr].keys()):
                if subs[id_usr][delo_num]['type'] not in dict_delo:
                    dict_delo[subs[id_usr][delo_num]['type']] = ''
                dict_delo[subs[id_usr][delo_num]['type']] += delo_num + ', '
    if dict_delo:
        for type_delo in list(dict_delo.keys()):
            answer_str += '{}: {}\n'.format(type_delo, dict_delo[type_delo].rsplit(',',1)[0])
    else:
        answer_str = u'Подписок пока нет' 
    return answer_str


def del_subs(subs, id_user):
    global delo
    for id_usr in list(subs.keys()):
        if id_usr == str(id_user):
            for delo_num in list(subs[id_usr].keys()):
                if delo_num == delo:
                    del subs[id_usr][delo_num]
