import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://kad.arbitr.ru/'
info = {
    'sug_cases': 'А41-76245/2019',
    'participant': '',
    'judge': '',
    'court': ''
}

driver = webdriver.Firefox(executable_path='../static/geckodriver')
driver.get('https://kad.arbitr.ru/')
action = webdriver.ActionChains(driver)


sug_cases = driver.find_element_by_id('sug-cases')
sug_cases = sug_cases.find_element_by_tag_name('input')
sug_cases.send_keys(info['sug_cases'])

if info['participant']:
    sug_participant = driver.find_element_by_id('sug-participants')
    sug_participant = sug_participant.find_element_by_tag_name('textarea')
    sug_participant.send_keys(info['participant'])

if info['judge']:
    judge = driver.find_element_by_id('sug-judges')
    judge = judge.find_element_by_tag_name('input')
    judge.send_keys(info['judge'])

if info['court']:
    court = driver.find_element_by_id('caseCourt')
    court = court.find_element_by_tag_name('input')
    court.send_keys(info['court'])
    court.send_keys(Keys.RETURN)

submit_button = driver.find_element_by_id('b-form-submit')
try:
    submit_button = WebDriverWait(submit_button, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, 'button'))
    )
    time.sleep(1)
    action.move_to_element(submit_button)
    action.click().perform()
    submit_button.click()
except TimeoutError:
    print('Cant click')

reset_button = driver.find_element_by_id('reset-link')
reset_button.click()

time.sleep(5)
driver.close()
