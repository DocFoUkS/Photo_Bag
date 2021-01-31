# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import random
import requests
from log_writer.writer import add_log


delo_num = ''


def document_initialised(driver):
    return driver.execute_script("return initialised")


def search_arbitr_delo():
    global delo_num
    add_log('Поиск дела {} в kad.arbitr'.format(delo_num))
    #print('Поиск дела {} в kad.arbitr'.format(delo_num))
    '''data = {'vyp3CaptchaToken': "", 'page': "", "query": inn_value, "region": 50, 'nameEq': 'on'}
    url = 'https://egrul.nalog.ru/'
    response = requests.post(url, data=data)
    response = json.loads(response.content)
    resul = requests.get('https://egrul.nalog.ru/search-result/{}'.format(response['t']))
    resp = json.loads(resul.content)
    inn = resp['rows'][0]['i']
    '''

    #delo_num = str('А41-72567/2018')

    profile = webdriver.FirefoxProfile(r'C:\Telegram_bot\selenium_driver')
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    profile.set_preference("general.useragent.override", "iPhone")
    options = webdriver.FirefoxOptions()
    options.headless = True
    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')

    browser = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, firefox_options=options)

    '''chrome_options = Options()
    chrome_options.add_argument('user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data')
    chrome_options.add_argument('profile-directory=Profile 1')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    chrome_options.add_experimental_option("useAutomationExtension", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    experimentalFlags = ['same-site-by-default-cookies@1','cookies-without-same-site-must-be-secure@1']
    chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
    chrome_options.add_experimental_option('localState',chromeLocalStatePrefs)
    
    browser = webdriver.Chrome(r'C:\Telegram_bot\selenium_driver\chromedriver.exe', options=chrome_options)'''
    
    #browser = webdriver.PhantomJS(r'C:\Telegram_bot\selenium_driver\phantomjs\bin\phantomjs.exe')
    #browser = webdriver.Ie(r'C:\Telegram_bot\selenium_driver\IEDriverServer.exe')
    time.sleep(2) # долго грузится - делаем задержку
    browser.get('https://m.kad.arbitr.ru/')
    print('Открылась страница')
    #browser.get('https://sur.ly/o/kad.arbitr.ru/AA000014')
    #WebDriverWait(browser, timeout=10).until(document_initialised)
    
    time.sleep(10)
    if len(browser.find_elements_by_css_selector('.b-promo_notification-popup-close')) > 0:
        act = browser.find_element_by_css_selector('.b-promo_notification-popup-close')
        act.send_keys(Keys.ESCAPE)

    act = browser.find_element_by_name('CaseNumbers[]')
    hover = ActionChains(browser).move_to_element(act)
    hover.perform()
    hover = ActionChains(browser).click_and_hold(act)
    hover.perform()
    act.click()
    time.sleep(5)
    a = tuple(str(delo_num))
    i = 0
    for i in range(len(a)):
        act.send_keys(a[i])
        time.sleep(random.uniform(0.1, 0.5))
        i += 1
    time.sleep(2)
    print('Введено дело')

    #act.send_keys(Keys.ENTER)
    act = browser.find_element_by_class_name('b-button').find_element_by_tag_name('input')
    hover = ActionChains(browser).move_to_element(act)
    hover.perform()
    #hover = ActionChains(browser).click_and_hold(act)
    #hover.perform()
    act.click()

    time.sleep(10)

    #browser.find_element_by_class_name('b-icon add').click()

    '''
    act = browser.find_element_by_css_selector('.b-button-container').find_element_by_tag_name('button')
    act.click()
    time.sleep(10)
    '''
    print('Push button search')

    shablon_dict = {}
    result_dict = {}
    mass_answer = []
    result = ''

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
                    link_delo = field_val.find_element_by_tag_name('a').get_attribute("href")
                    res_link = ''
                    if link_delo.count('https://') > 1:
                        for el_link in link_delo.split('https://'):
                            if el_link != 'm.kad.arbitr.ru/':
                                res_link += 'https://' + el_link + ', '
                    else:
                        res_link = link_delo
                    result_dict[irow] = 'Карточка дела: {}'.format(res_link.rsplit(',',1)[0])
                result_dict[irow_val] += field_val.text.replace('\n', ' ')
                irow_val += 1
            mass_answer.append(result_dict)
            result_dict = shablon_dict
            irow_val = 0

    if len(browser.find_elements_by_id('search_results')) > 0:
        if len(browser.find_element_by_id('search_results').find_elements_by_tag_name('li')) > 0:
            table = browser.find_element_by_id('search_results').find_element_by_tag_name('li')
            result = ''
            irow = 0
            for val_res in table.find_elements_by_tag_name('div'):
                if irow == 1:
                    result += 'Дело: {}\nКарточка дела: {}\n'.format(val_res.text, val_res.find_element_by_tag_name('a').get_attribute("href"))
                else:
                    result += val_res.text + '\n'
                irow += 1

    if mass_answer != []:
        for rows in mass_answer:
            for element in list(rows.keys()):
                result += rows[element] + '\n'
            result += '\n'
    if result.lower().count('дело') == 0:
        result = 'Данные по запросу не найдены'

    browser.quit()
    print(result)
    return result


def req_post():
    http = requests.Session()
    http.headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': '*/*',
            'Content-Length': '145',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            #'Cookie': '__utma=14300007.1560979077.1419681550.1419681550.1419681550.1; __utmz=14300007.1419681550.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ASP.NET_SessionId=o33wghgnfxi041kx3nsruwki; userId=2bcd95e5-4511-4ecb-8b12-519cbce24a86:s0hOMqJTdq/CE7opFdCBvw==; __utmt=1; __utma=228081543.1213039978.1419665530.1421072267.1421072267.10; __utmb=228081543.2.10.1421072267; __utmc=228081543; __utmz=228081543.1421072267.9.5.utmcsr=localhost:8180|utmccn=(referral)|utmcmd=referral|utmcct=/autokad/src/nkb-app/; aUserId=832fe384-d14c-4bd9-83fb-61aa7182954c:NGEVLG4bQfvBFguC16bdVQ==',
            'Cookie': 'CUID=e1422c95-7796-4649-94ad-b55feba055b0:obfWLJC5ouhmxQKwsfARwg==; _ga=GA1.2.74192253.1603974996; _fbp=fb.1.1603974997228.1940624049; _ym_uid=1603974998889550486; _ym_d=1603974998; ARRAffinityKAD=eee139e156b8452173b3cdfaec7c8e8b03991ad1b41102b9083e3131199e0e6c; ASP.NET_SessionId=wtkxkm5drt4vc2v3yy4poh24; _gid=GA1.2.1105621938.1607627562; _ym_isad=2; pr_fp=c7c6d4fab81d09fbe2688af0f3dc57857ff7eaddb782b1a5cbd3ae26f0108be6; rcid=997ad366-6d17-4e43-b0ce-6c09df0273ff; wasm=47aea3d8999801003b350e876a1878ea',
            'x-date-format': 'iso',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kad.arbitr.ru',
            'Referer': 'https://kad.arbitr.ru/',
            'Host': 'kad.arbitr.ru'
        }
    )
    
    '''get_ping = http.get('https://kad.arbitr.ru/Wasm/api/v1/wasm.js?_=1608147976863')
    print(get_ping)'''

    url = "https://kad.arbitr.ru/Kad/SearchInstances"

    parameter = {
        "Page": 1,
        "Count": 25,
        "Courts": [],
        "DateFrom": None,
        "DateTo": None,
        "Sides": [],
        "Judges": [],
        "CaseNumbers": ["А41-72567/2017"],
        "WithVKSInstances": False
    }

    '''captcha = http.get('https://m.kad.arbitr.ru/Recaptcha/IsNeedShowCaptcha?_=1604090246295', verify=False)
    print(captcha.text)'''
    html_code = http.post(url, data=parameter, verify=False).text
    print(html_code)


'''if __name__ == '__main__':
    #delo_num = input('Введите номер дела: ')
    search_arbitr_delo()
    #req_post()'''
