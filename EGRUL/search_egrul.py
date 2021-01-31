# -*- coding: utf-8 -*-

import requests
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time


def egrul(egreg, egfam, dan):
    if egreg == '-':
        egreg = ''
    data = {'vyp3CaptchaToken': "", 'page': "", "query": egfam, "region": egreg, 'nameEq': 'on'}
    url = 'https://egrul.nalog.ru/'
    response = requests.post(url, data=data)
    response = json.loads(response.content)
    resul = requests.get('https://egrul.nalog.ru/search-result/{}'.format(response['t']))
    resp = json.loads(resul.content)

    suma = ''
    ids = []
    k = 1
    stroka = ''
    for i in resp['rows']:
        suma += i['t'] + ' '
        if 'e' in i.keys():
            stroka += """{}. {}
    ОГРНИП: {}, ИНН: {}, Дата присвоения ОГРНИП: {}, Дата прекращения деятельности: {}\n""".format(k,i['n'],i['o'],i['i'],i['r'],i['e'])
        else:
            stroka += """{}. {}
    ОГРНИП: {}, ИНН: {}, Дата присвоения ОГРНИП: {}\n""".format(k,i['n'],i['o'],i['i'],i['r'])
        k += 1
        if k % 11 == 0:
            break
    stroka += 'Показано {} из {} записей'.format(k-1, len(resp['rows']))

    dan = suma

    return stroka, k-1, dan

def down_egrul(egreg, egfam, nom):
    if egreg == '-':
        egreg = ''
    data = {'vyp3CaptchaToken': "", 'page': "", "query": egfam, "region": egreg, 'nameEq': 'on'}
    url = 'https://egrul.nalog.ru/'
    response = requests.post(url, data=data)
    response = json.loads(response.content)
    resul = requests.get('https://egrul.nalog.ru/search-result/{}'.format(response['t']))
    resp = json.loads(resul.content)

    inn_val = resp['rows'][int(nom) - 1].get('i', '0')
    region_val = resp['rows'][int(nom) - 1].get('o', '0')

    load_egrul_pdf(inn_val)

    for pdf_file in os.listdir(r'C:\Telegram_bot\egr'):
        egr = pdf_file
        break

    return r'C:\Telegram_bot\egr\{}'.format(egr)


def load_egrul_pdf(inn_value):
    inn = str(inn_value)

    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", r'C:\Telegram_bot\egr')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    profile.set_preference("browser.download.manager.showWhenStarting", False);
    profile.set_preference("browser.download.manager.focusWhenStarting", False);  
    profile.set_preference("browser.download.useDownloadDir", True);
    profile.set_preference("browser.helperApps.alwaysAsk.force", False);
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False);
    profile.set_preference("browser.download.manager.closeWhenDone", True);
    profile.set_preference("browser.download.manager.showAlertOnComplete", False);
    profile.set_preference("browser.download.manager.useWindow", False);
    profile.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False);
    profile.set_preference("pdfjs.disabled", True);

    browser = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)
    time.sleep (2) # долго грузится - делаем задержку
    browser.get ('https://egrul.nalog.ru/')

    act = browser.find_element_by_id('query')
    act.click()
    time.sleep (1)
    a = tuple(str(inn))
    # вводим посимвольно в строку ОГРН, т.к. ввод сразу всего ОГРН не корректно обрабатывается
    i=0
    for i in range (len(a)):
        act.send_keys(a[i])
        #time.sleep (0.1)
        i+=1
    act = browser.find_element_by_css_selector('.btn-search')
    act.click()
    time.sleep (1)
    act = browser.find_element_by_css_selector('button.btn-with-icon:nth-child(2)')
    act.click()
    time.sleep (3)
    act = browser.find_element_by_id('query')
    act.click()

    browser.quit()
