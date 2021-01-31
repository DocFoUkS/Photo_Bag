import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SudrfCourts:
    def __init__(self, info):
        self.info = info
        headers = dict(DesiredCapabilities.PHANTOMJS)
        headers["phantomjs.page.settings.userAgent"] = \
            ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36")
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        self.url = 'https://sudrf.ru/index.php?id=300&var=true#sp'
        self.driver = webdriver.Firefox(executable_path='../static/geckodriver', firefox_options=options)
        self.result = None

    def get_result(self):
        self.driver.get(self.url)

        subject = Select(self.driver.find_element_by_id('court_subj'))
        subject.select_by_value(info['subject'])

        try:
            court = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, 'suds_subj'))
            )
            court = Select(court)
            court.select_by_visible_text(info['court_name'])
        except TimeoutError:
            pass

        case_number = self.driver.find_element_by_id('num_df')
        case_number.send_keys(info['case_number'])

        submit = self.driver.find_elements_by_tag_name('input')
        submit[-2].click()

        try:
            result = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, 'delo_mir'))
            )
            result = result.find_element_by_tag_name('tbody')
            result = result.find_elements_by_tag_name('td')
            self.result = '\n'.join([res.text for res in result])
        except TimeoutError:
            pass

        self.driver.close()
        return self.result


info = {
    'case_number': '2-1521/2019',
    'subject': '50',
    'court_name': 'Судебный участок № 332 мирового судьи Химкинского судебного района Московской области'
}
