# -*- coding: utf-8 -*-

import codecs
import json
import time

import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

region = 0
sud_name = ''
delo_num = 0


def load_sud_dict():
    with codecs.open(r'C:\Telegram_bot\MOSGORSUD\mir_sud_codes.json', 'r', encoding='utf-8') as jsop:
        return json.load(jsop)



def search_mir_delo():
    global region
    global sud_name
    global delo_num

    if sud_name == '-' or sud_name == '':
        return 'Не введено наименование мирового суда'
    if delo_num == '' or delo_num == '-':
        return 'Не введен номер дела'

    http = requests.Session()
    http.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

    dict_sud = load_sud_dict()
    sud_code = ''

    print(sud_name)

    if sud_name[-1:].isdigit():
        sud_name += ' '
    print(sud_name)
    if sud_name.count('MS') == 1:
        sud_code = sud_name
    else:
        for suds in list(dict_sud[str(region)].keys()):
            if suds.replace(' # ', ' ').replace(' № ', ' ').count(sud_name.replace(' # ', ' ').replace(' № ', ' ').upper())>0:
                sud_code = dict_sud[str(region)][suds]
    print(sud_code)

    url = "https://sudrf.ru/index.php?id=300&act=go_sp_search&searchtype=sp&mvnkod={code}&var=true&num_d={delo}&court_subj={region}&suds_subj={code}&num_df={delo}".format(delo=delo_num, code=sud_code, region=region)

    #browser = webdriver.Firefox()
    options = Options()
    options.binary_location = r"geckodriver.exe"

    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", r'C:\FoUkS\FL\IP_bot')
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
    time.sleep(1) # долго грузится - делаем задержку
    browser.get(url)

    enter_delo = browser.find_element_by_id('num_df')
    enter_delo.click()
    time.sleep(1)
    a = tuple(str(delo_num))
    # вводим посимвольно в строку ОГРН, т.к. ввод сразу всего ОГРН не корректно обрабатывается
    i=0
    for i in range(len(a)):
        enter_delo.send_keys(a[i])
        #time.sleep (0.1)
        i+=1

    time.sleep(4)
    start_search = browser.find_element_by_css_selector('#courtGuideTbl > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > input:nth-child(1)')
    start_search.click()
    time.sleep(4)
    '''
    html_code = http.get(url, verify=False).text
    with codecs.open(r'C:\Telegram_bot\test_mit_html.html', 'w', encoding='utf-8') as filewrite:
        filewrite.write(html_code)

    soup = BS(html_code, 'lxml')
    '''
    result = 'К сожалению ничего не нашлось'

    #if soup.find('div', {'id': 'delo_mir'}):
    if len(browser.find_elements_by_id('delo_mir')) > 0:
        table = browser.find_element_by_id('delo_mir')
        dict_result = {}
        result = ''
        ifield = 0
        for field_nm in table.find_elements_by_tag_name('tr'):
            for field_nm_thread in field_nm.find_elements_by_tag_name('td'):
                dict_result[ifield] = field_nm_thread.text.replace('\n', ' ') + ': '
                ifield += 1
            break
        ifield_v = 0
        result = ''
        for field_val in table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'):
            link_delo = ''
            for field_val_head in field_val.find_elements_by_tag_name('td'):
                if ifield_v == 0:
                    link_delo = 'Ссылка на дело: ' + field_val_head.find_element_by_tag_name('a').get_attribute("href")
                result += dict_result[ifield_v] + field_val_head.text + '\n'
                ifield_v += 1
            result += link_delo + '\n\n'
            ifield_v = 0

    browser.quit()

    return result.rsplit('\n\n', 1)[0]
