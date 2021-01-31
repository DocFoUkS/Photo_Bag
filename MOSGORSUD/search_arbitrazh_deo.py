# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import random


delo_num = ''


def search_arbitr_delo():
    global delo_num
    '''data = {'vyp3CaptchaToken': "", 'page': "", "query": inn_value, "region": 50, 'nameEq': 'on'}
    url = 'https://egrul.nalog.ru/'
    response = requests.post(url, data=data)
    response = json.loads(response.content)
    resul = requests.get('https://egrul.nalog.ru/search-result/{}'.format(response['t']))
    resp = json.loads(resul.content)
    inn = resp['rows'][0]['i']
    '''

    #delo_num = str('А41-72567/2018')

    #profile = webdriver.FirefoxProfile(r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\6d694y0j.default-release')
    #options = webdriver.FirefoxOptions()
    #binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')

    #browser = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, firefox_options=options)

    chrome_options = Options()
    chrome_options.add_argument('user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data')
    chrome_options.add_argument('profile-directory=Profile 1')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    browser = webdriver.Chrome(r'C:\Telegram_bot\selenium_driver\chromedriver.exe', options=chrome_options)

    #browser = webdriver.PhantomJS(r'C:\Telegram_bot\selenium_driver\phantomjs\bin\phantomjs.exe')
    #browser = webdriver.Ie(r'C:\Telegram_bot\selenium_driver\IEDriverServer.exe')
    time.sleep(2) # долго грузится - делаем задержку
    browser.get('https://kad.arbitr.ru/')
    
    time.sleep(10)
    if len(browser.find_elements_by_css_selector('.b-promo_notification-popup-close')) > 0:
        act = browser.find_element_by_css_selector('.b-promo_notification-popup-close')
        act.send_keys(Keys.ESCAPE)

    act = browser.find_element_by_id('sug-cases').find_element_by_tag_name('input')
    act.click()
    time.sleep(5)
    a = tuple(str(delo_num))
    i = 0
    for i in range(len(a)):
        act.send_keys(a[i])
        time.sleep(random.uniform(0.1, 0.5))
        i += 1
    time.sleep(2)

    act.send_keys(Keys.ENTER)

    time.sleep(10)

    #browser.find_element_by_class_name('b-icon add').click()

    print('Enter delo')
    '''
    act = browser.find_element_by_css_selector('.b-button-container').find_element_by_tag_name('button')
    act.click()
    time.sleep(10)
    '''
    print('Push button search')

    shablon_dict = {}
    result_dict = {}
    mass_answer = []

    if len(browser.find_elements_by_class_name('b-results')) > 0:
        table = browser.find_element_by_class_name('b-results')
        irow = 0
        for field_name in table.find_element_by_id('b-cases-theader').find_elements_by_tag_name('div'):
            result_dict[irow] = field_name.text.replace('\n', ' ') + ': '
            irow += 1
        shablon_dict = result_dict
        irow_val = 0
        for field_values in table.find_element_by_class_name('b-cases_wrapper').find_elements_by_tag_name('tr'):
            for field_val in field_values.find_elements_by_tag_name('td'):
                if irow_val == 0:
                    result_dict[irow] = 'Карточка дела: {}'.format(field_val.find_element_by_tag_name('a').get_attribute("href"))
                result_dict[irow_val] += field_val.text.replace('\n', ' ')
                irow_val += 1
            mass_answer.append(result_dict)
            result_dict = shablon_dict
            irow_val = 0

    result = ''
    for rows in mass_answer:
        for element in list(rows.keys()):
            result += rows[element] + '\n'
        result += '\n'
    if result.lower().count('дело') == 0:
        result = 'Данные не нашлись'

    browser.quit()
    return result

'''
if __name__ == '__main__':
    delo_num = input('Введите номер дела: ')
    load_egrul_pdf(delo_num)
'''
