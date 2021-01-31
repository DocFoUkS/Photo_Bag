# -*- coding: utf-8 -*-

import requests
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time


def load_egrul_pdf(inn_value):
    '''data = {'vyp3CaptchaToken': "", 'page': "", "query": inn_value, "region": 50, 'nameEq': 'on'}
    url = 'https://egrul.nalog.ru/'
    response = requests.post(url, data=data)
    response = json.loads(response.content)
    resul = requests.get('https://egrul.nalog.ru/search-result/{}'.format(response['t']))
    resp = json.loads(resul.content)
    inn = resp['rows'][0]['i']
    '''

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

    #browser = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, executable_path=r"C:\Telegram_bot\geckodriver.exe")
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
