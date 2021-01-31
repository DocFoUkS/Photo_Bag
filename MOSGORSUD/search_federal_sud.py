# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as BS
import codecs
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

region = 0
sud_ish = ''
city_ish = ''
sud_fed_ish = ''
delo_num = ''
storona = ''


def load_federal_sud_code():
    with codecs.open(r'C:\Telegram_bot\MOSGORSUD\federal_sud_code.json', 'r', encoding='utf-8') as jsop:
        return json.load(jsop)


def search_federal_sud_contact():
    global region
    global sud_ish
    global city_ish

    if sud_ish == '-':
        sud_ish = ''
    if city_ish == '-':
        city_ish =''

    http = requests.Session()
    http.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

    dict_bukv = {'Ђ': r'%80', 'Ѓ': r'%81', '‚': r'%82', 'ѓ': r'%83', '„': r'%84', '…': r'%85', '†': r'%86', '‡': r'%87', '€': r'%88', '‰': r'%89', 'Љ': r'%8A', '‹': r'%8B', 'Њ': r'%8C', 'Ќ': r'%8D', 'Ћ': r'%8E', 'Џ': r'%8F', 'Ђ': r'%90', '‘': r'%91', '’': r'%92', '“': r'%93', '”': r'%94', '•': r'%95', '–': r'%96', '—': r'%97', 'Начало строки': r'%98', '™': r'%99', 'љ': r'%9A', '›': r'%9B', 'њ': r'%9C', 'ќ': r'%9D', 'ћ': r'%9E', 'џ': r'%9F', 'Неразрывный пробел': r'%A0', 'Ў': r'%A1', 'ў': r'%A2', 'Ј': r'%A3', '¤': r'%A4', 'Ґ': r'%A5', '¦': r'%A6', '§': r'%A7', 'Ё': r'%A8', '©': r'%A9', 'Є': r'%AA', '«': r'%AB', '¬': r'%AC', 'Мягкий перенос': r'%AD', '®': r'%AE', 'Ї': r'%AF', '°': r'%B0', '±': r'%B1', 'І': r'%B2', 'і': r'%B3', 'ґ': r'%B4', 'µ': r'%B5', '¶': r'%B6', '·': r'%B7', 'ё': r'%B8', '№': r'%B9', 'є': r'%BA', '»': r'%BB', 'ј': r'%BC', 'Ѕ': r'%BD', 'ѕ': r'%BE', 'ї': r'%BF', 'А': r'%C0', 'Б': r'%C1', 'В': r'%C2', 'Г': r'%C3', 'Д': r'%C4', 'Е': r'%C5', 'Ж': r'%C6', 'З': r'%C7', 'И': r'%C8', 'Й': r'%C9', 'К': r'%CA', 'Л': r'%CB', 'М': r'%CC', 'Н': r'%CD', 'О': r'%CE', 'П': r'%CF', 'Р': r'%D0', 'С': r'%D1', 'Т': r'%D2', 'У': r'%D3', 'Ф': r'%D4', 'Х': r'%D5', 'Ц': r'%D6', 'Ч': r'%D7', 'Ш': r'%D8', 'Щ': r'%D9', 'Ъ': r'%DA', 'Ы': r'%DB', 'Ь': r'%DC', 'Э': r'%DD', 'Ю': r'%DE', 'Я': r'%DF', 'а': r'%E0', 'б': r'%E1', 'в': r'%E2', 'г': r'%E3', 'д': r'%E4', 'е': r'%E5', 'ж': r'%E6', 'з': r'%E7', 'и': r'%E8', 'й': r'%E9', 'к': r'%EA', 'л': r'%EB', 'м': r'%EC', 'н': r'%ED', 'о': r'%EE', 'п': r'%EF', 'р': r'%F0', 'с': r'%F1', 'т': r'%F2', 'у': r'%F3', 'ф': r'%F4', 'х': r'%F5', 'ц': r'%F6', 'ч': r'%F7', 'ш': r'%F8', 'щ': r'%F9', 'ъ': r'%FA', 'ы': r'%FB', 'ь': r'%FC', 'э': r'%FD', 'ю': r'%FE', 'я': r'%FF'}

    sud = ''
    for el in sud_ish.replace(' ','+'):
        sud+=dict_bukv.get(el, el)
    city = ''
    for el in city_ish.replace(' ', '+'):
        city+=dict_bukv.get(el, el)

    url = "https://sudrf.ru/index.php?id=300&act=go_search&searchtype=fs&court_name={}&court_subj={}&fs_city={}&fs_street=&court_type=0&court_okrug=0&vcourt_okrug=0".format(sud, region, city)

    result = 'К сожалению ничего не нашлось'

    html_code = http.get(url, verify=False).text

    soup = BS(html_code, 'lxml')
    if soup.find('table', {'class': "msSearchResultTbl msFullSearchResultTbl"}):
        table = soup.find('table', {'class': "msSearchResultTbl msFullSearchResultTbl"})
        rows_many = 1
        i = 0
        result = ''

        for sud in table.findAll('td'):
            if i>rows_many and sud.text.count('Классификационный код:') == 1:
                if int(sud.text.split('Классификационный код: ')[1][:2]) == region:
                    result += sud.text.split('\n\n')[0]+':\nКлассификационный код:{}\n'.format(sud.text.split('Классификационный код:')[1].replace('Адрес:','\nАдрес:').replace('Телефон:','\nТелефон:').replace('E-mail:','\nE-mail:'))
            i += 1
    else:
        table = soup.find('ul', {'class': "search-results"})
        result = ''

        for sud in table.findAll('li'):
            for info in sud.findAll('div'):
                if info.text.count('Классификационный код:') == 1:
                    if int(info.text.split('Классификационный код: ')[1][:2])==region:
                        result += sud.text.split('\n\n')[0] + ':\nКлассификационный код:{}\n\n'.format(info.text.split('Классификационный код:')[1].replace('Адрес:','\nАдрес:').replace('Телефон:','\nТелефон:').replace('E-mail:','\nE-mail:').replace('Официальный сайт:','\nОфициальный сайт:'))
    return result


def load_info(browser, table_tag):
    table = browser.find_element_by_id(table_tag)
    dict_result = {}
    ifield = 0
    for field_nm in table.find_element_by_css_selector('.law-case-table > thead:nth-child(1)').find_elements_by_tag_name('td'):
        dict_result[ifield] = field_nm.text.replace('\n',' ') + ': '
        ifield +=1
    ifield_v = 0
    result = ''
    for field_val in table.find_element_by_css_selector('.law-case-table > tbody:nth-child(2)').find_elements_by_tag_name('td'):
        if ifield_v == 1:
            dict_result[ifield] = 'Ссылка на дело: ' + field_val.find_element_by_tag_name('a').get_attribute("href")
        dict_result[ifield_v] += field_val.text + '\n'
        ifield_v += 1

    result = ''
    for el in list(dict_result.keys()):
        result += dict_result[el]
    return result


def load_info_v2(browser, table_tag):
    table = browser.find_element_by_id(table_tag)
    dict_result = {}
    ifield = 0
    for field_nm in table.find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr'):
        for field_nm_head in field_nm.find_elements_by_tag_name('td'):
            dict_result[ifield] = field_nm_head.text.replace('\n', ' ') + ': '
            ifield += 1
        break
    ifield_v = 0
    irow = 0
    result = ''
    for field_val in table.find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr'):
        if irow > 0:
            link_delo = ''
            for field_val_head in field_val.find_elements_by_tag_name('td'):
                if ifield_v == 1:
                    link_delo = 'Ссылка на дело: ' + field_val_head.find_element_by_tag_name('a').get_attribute("href")
                result += dict_result[ifield_v] + field_val_head.text + '\n'
                ifield_v += 1
            result += link_delo + '\n\n'
            ifield_v = 0
        irow += 1

    return result.rsplit('\n\n', 1)[0]


def search_federal_sud_delo():
    global region
    global sud_fed_ish
    global delo_num
    global storona

    if len(str(region)) == 3:
        region = int(str(region)[1:])

    dict_fed_sud = load_federal_sud_code()

    result = 'Не получилось найти информацию по делам'
    storona_convert = ''

    sud_code = ''
    if sud_fed_ish[:2].isdigit() and int(sud_fed_ish[:2]) == region:
        sud_code = sud_fed_ish
    else:
        for el in list(dict_fed_sud[str(region)].keys()):
            if el.count(sud_fed_ish.upper()) == 1:
                sud_code = dict_fed_sud[str(region)][el]

    if sud_code == '' or sud_code == '-':
        return result + '\nВведите наименование суда'

    if delo_num == '' or delo_num == '-':
        return result + '\nВведите номер дела'

    if storona == '-':
        storona = ''

    if storona != '':
        dict_bukv = {'Ђ': r'%80', 'Ѓ': r'%81', '‚': r'%82', 'ѓ': r'%83', '„': r'%84', '…': r'%85', '†': r'%86', '‡': r'%87', '€': r'%88', '‰': r'%89', 'Љ': r'%8A', '‹': r'%8B', 'Њ': r'%8C', 'Ќ': r'%8D', 'Ћ': r'%8E', 'Џ': r'%8F', 'Ђ': r'%90', '‘': r'%91', '’': r'%92', '“': r'%93', '”': r'%94', '•': r'%95', '–': r'%96', '—': r'%97', 'Начало строки': r'%98', '™': r'%99', 'љ': r'%9A', '›': r'%9B', 'њ': r'%9C', 'ќ': r'%9D', 'ћ': r'%9E', 'џ': r'%9F', 'Неразрывный пробел': r'%A0', 'Ў': r'%A1', 'ў': r'%A2', 'Ј': r'%A3', '¤': r'%A4', 'Ґ': r'%A5', '¦': r'%A6', '§': r'%A7', 'Ё': r'%A8', '©': r'%A9', 'Є': r'%AA', '«': r'%AB', '¬': r'%AC', 'Мягкий перенос': r'%AD', '®': r'%AE', 'Ї': r'%AF', '°': r'%B0', '±': r'%B1', 'І': r'%B2', 'і': r'%B3', 'ґ': r'%B4', 'µ': r'%B5', '¶': r'%B6', '·': r'%B7', 'ё': r'%B8', '№': r'%B9', 'є': r'%BA', '»': r'%BB', 'ј': r'%BC', 'Ѕ': r'%BD', 'ѕ': r'%BE', 'ї': r'%BF', 'А': r'%C0', 'Б': r'%C1', 'В': r'%C2', 'Г': r'%C3', 'Д': r'%C4', 'Е': r'%C5', 'Ж': r'%C6', 'З': r'%C7', 'И': r'%C8', 'Й': r'%C9', 'К': r'%CA', 'Л': r'%CB', 'М': r'%CC', 'Н': r'%CD', 'О': r'%CE', 'П': r'%CF', 'Р': r'%D0', 'С': r'%D1', 'Т': r'%D2', 'У': r'%D3', 'Ф': r'%D4', 'Х': r'%D5', 'Ц': r'%D6', 'Ч': r'%D7', 'Ш': r'%D8', 'Щ': r'%D9', 'Ъ': r'%DA', 'Ы': r'%DB', 'Ь': r'%DC', 'Э': r'%DD', 'Ю': r'%DE', 'Я': r'%DF', 'а': r'%E0', 'б': r'%E1', 'в': r'%E2', 'г': r'%E3', 'д': r'%E4', 'е': r'%E5', 'ж': r'%E6', 'з': r'%E7', 'и': r'%E8', 'й': r'%E9', 'к': r'%EA', 'л': r'%EB', 'м': r'%EC', 'н': r'%ED', 'о': r'%EE', 'п': r'%EF', 'р': r'%F0', 'с': r'%F1', 'т': r'%F2', 'у': r'%F3', 'ф': r'%F4', 'х': r'%F5', 'ц': r'%F6', 'ч': r'%F7', 'ш': r'%F8', 'щ': r'%F9', 'ъ': r'%FA', 'ы': r'%FB', 'ь': r'%FC', 'э': r'%FD', 'ю': r'%FE', 'я': r'%FF'}

        storona_convert = ''
        for el in storona.replace(' ', '+'):
            storona_convert += dict_bukv.get(el, el)

    url = "https://sudrf.ru/index.php?id=300&act=go_search&searchtype=sp&court_subj={}&suds_subj={}&num_d={}&f_name={}".format(region, sud_code, delo_num, storona_convert)

    # browser = webdriver.Firefox()
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
    time.sleep(2) # долго грузится - делаем задержку
    browser.get(url)

    time.sleep(2)
    start_search = browser.find_element_by_css_selector('#court_searchfs > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(2) > input:nth-child(1)')
    start_search.click()
    time.sleep(10)

    if len(browser.find_elements_by_id('resultTable')) > 0:
        result = load_info(browser, 'resultTable')
    elif len(browser.find_elements_by_id('tablcont')) > 0:
        result = load_info_v2(browser, 'tablcont')
    else:
        pass
    browser.quit()

    return result
