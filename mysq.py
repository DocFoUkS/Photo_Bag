import sqlite3
import time
import requests
import json
from bs4 import BeautifulSoup as bs
from selenium_pdf_load import egrul_load
import os

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': '_ym_uid=1585566028502117968; _ym_d=1585566028; _ym_isad=2; _ym_visorc_1187093=b; c-dis=1; sputnik_session=1585659793406|17',
    'Host': 'mos-gorsud.ru',
    'Referer': 'https://mos-gorsud.ru/search?formType=shortForm&courtAlias=&uid=&instance=&processType=&letterNumber=&caseNumber=2-4096%2F2018&participant=',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}


class Polzo(object):
    def __init__(self, idk):
        self.token = 'Z2OfN7weWTW5'
        self.db_path = "C:/Telegram_bot/polzo.db"
        print(self.db_path)
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        self.timeog = 60
        try:
            cursor.execute("INSERT INTO polz (id,step,adminc) VALUES ('{0}','0','0')".format(idk))
            conn.commit()
            k = [[0, 0, 0]]
        except Exception:
            cursor.execute("SELECT * FROM polz where id = {}".format(idk))
            k = cursor.fetchall()
            conn.commit()
        self.idk = idk
        self.step = k[0][1]
        self.admin = k[0][2]

        try:
            cursor.execute("INSERT INTO egrul (id,fam,reg,dan,inn,ogrn) VALUES ('{0}','0','0','0','0','0')".format(idk))
            conn.commit()
            k = [[0, 0, 0, 0, 0, 0]]
        except Exception:
            cursor.execute("SELECT * FROM egrul where id = {}".format(idk))
            k = cursor.fetchall()
            conn.commit()
        self.egfam = k[0][1]
        self.egreg = k[0][2]
        self.dan = k[0][3]
        
        try:
            cursor.execute("INSERT INTO fspphys (region,firstname,secondname,lastname,birthdate,id,time,key) VALUES ('0','0','0','0','0','{0}',0,'0')".format(idk))
            conn.commit()
            k = [[0, 0, 0, 0, 0, 0, 0, 0]]
        except Exception:
            cursor.execute("SELECT * FROM fspphys where id = {}".format(idk))
            k = cursor.fetchall()
            conn.commit()
        self.fspreg = k[0][0]
        self.firstname = k[0][1]
        self.secondname = k[0][2]
        self.lastname = k[0][3]
        self.birthdate = k[0][4]
        self.timehys = k[0][6]
        self.keyhys = k[0][7]
        
        try:
            cursor.execute(f"INSERT INTO fsppleg (id,region,name,address,time,key) VALUES ('{idk}','0','0','0',0,'0')")
            conn.commit()
            k = [[0, 0, 0, 0, 0, 0]]
        except Exception:
            cursor.execute("SELECT * FROM fsppleg where id = {}".format(idk))
            k = cursor.fetchall()
            conn.commit()

        self.fsplegreg = k[0][1]
        self.name = k[0][2]
        self.address = k[0][3]
        self.timeleg = k[0][4]
        self.keyleg = k[0][5]
        
        try:
            cursor.execute("INSERT INTO sudrf (id,uid,vhod,nom,stor) VALUES ('{0}','0','0','0','0')".format(idk))
            conn.commit()
            k = [[0, 0, 0, 0, 0]]
        except Exception:
            cursor.execute("SELECT * FROM sudrf where id = {}".format(idk))
            k = cursor.fetchall()
            conn.commit()

        self.uid = k[0][1]
        self.vhod = k[0][2]
        self.nom = k[0][3]
        self.stor = k[0][4]

        try:
            cursor.execute(f"INSERT INTO fsppip (id,number,time,key) VALUES ('{idk}','0','0','0')")
            conn.commit()
            k = [[0, 0, 0, 0]]
        except Exception:
            cursor.execute(f"SELECT * FROM fsppip where id = {idk}")
            k = cursor.fetchall()
            conn.commit()
        self.numberip = k[0][1]
        self.timeip = k[0][2]
        self.keyip = k[0][3]

    def set_egrul_fam(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE egrul SET fam = '{vle}' WHERE id = '{self.idk}'")
        #self.inn_val, self.oghn_val = 
        self.egfam = vle
        conn.commit()

    def set_egrul_reg(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE egrul SET reg = '{vle}' WHERE id = '{self.idk}'")
        self.egreg = vle
        conn.commit()
        
    def set_egrul_dan(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE egrul SET dan = '{vle}' WHERE id = '{self.idk}'")
        self.dan = vle
        conn.commit()

    def set_fspphys_reg(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fspphys SET region = '{vle}' WHERE id = '{self.idk}'")
        self.fspreg = vle
        conn.commit()
        
    def set_fsppip_number(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fsppip SET number = '{vle}' WHERE id = '{self.idk}'")
        self.numberip = vle
        conn.commit()

    def set_fspphys_firstname(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fspphys SET firstname = '{vle}' WHERE id = '{self.idk}'")
        self.firstname = vle
        conn.commit()

    def set_fspphys_secondname(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fspphys SET secondname = '{vle}' WHERE id = '{self.idk}'")
        self.secondname = vle
        conn.commit()
        
    def set_fspphys_lastname(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fspphys SET lastname = '{vle}' WHERE id = '{self.idk}'")
        self.lastname = vle
        conn.commit()

    def set_fspphys_birthdate(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fspphys SET birthdate = '{vle}' WHERE id = '{self.idk}'")
        self.birthdate = vle
        conn.commit()

    def set_fsppleg_reg(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fsppleg SET region = '{vle}' WHERE id = '{self.idk}'")
        self.fsplegreg = vle
        conn.commit()
        
    def set_fsppleg_name(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fsppleg SET name = '{vle}' WHERE id = '{self.idk}'")
        self.name = vle
        conn.commit()
        
    def set_fsppleg_address(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE fsppleg SET address = '{vle}' WHERE id = '{self.idk}'")
        self.address = vle
        conn.commit()
        
    def set_sudrf_uid(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE sudrf SET uid = '{vle}' WHERE id = '{self.idk}'")
        self.uid = vle
        conn.commit()
        
    def set_sudrf_vhod(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE sudrf SET vhod = '{vle}' WHERE id = '{self.idk}'")
        self.vhod = vle
        conn.commit()
        
    def set_sudrf_nom(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE sudrf SET nom = '{vle}' WHERE id = '{self.idk}'")
        self.nom = vle
        conn.commit()
        
    def set_sudrf_stor(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE sudrf SET stor = '{vle}' WHERE id = '{self.idk}'")
        self.stor = vle
        conn.commit()

    def set_step(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute("UPDATE polz SET step = '{0}' WHERE id = '{1}'".format(vle, self.idk))
        self.step = vle
        conn.commit()

    def set_adm(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute("UPDATE polz SET adminc = '{0}' WHERE id = '{1}'".format(vle, self.idk))
        cursor.execute("UPDATE polz SET adminc = '{1}' WHERE id = '{0}'".format(vle, self.idk))
        self.admin = vle
        conn.commit()

    def ub_adm(self, vle):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute("UPDATE polz SET step = '0' WHERE id = '{}'".format(vle))
        cursor.execute("UPDATE polz SET adminc = '0' WHERE id = '{}'".format(vle))
        cursor.execute("UPDATE polz SET adminc = '0' WHERE id = '{}'".format(self.idk))
        self.admin = 0
        conn.commit()

    def search_value_for_egrul(self):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute(f"UPDATE egrul SET reg = '{vle}' WHERE id = '{self.idk}'")
        self.egreg = vle
        conn.commit()

    def delq(self):
        conn = sqlite3.connect(self.db_path) 
        cursor = conn.cursor()
        cursor.execute("DELETE FROM polz WHERE id = {}".format(self.idk))
        cursor.execute("DELETE FROM egrul WHERE id = {}".format(self.idk))
        cursor.execute("DELETE FROM fspphys WHERE id = {}".format(self.idk))
        cursor.execute("DELETE FROM fsppleg WHERE id = {}".format(self.idk))
        cursor.execute("DELETE FROM sudrf WHERE id = {}".format(self.idk))
        conn.commit()

    def egrul(self):
        if self.egreg == '-':
            self.egreg = ''
        data = {'vyp3CaptchaToken': "", 'page': "", "query": self.egfam, "region": self.egreg, 'nameEq': 'on'}
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
            
        self.dan = suma

        return stroka, k-1

    def down_egrul(self, nom):
        if self.egreg == '-':
            self.egreg = ''
        data = {'vyp3CaptchaToken': "", 'page': "", "query": self.egfam, "region": self.egreg, 'nameEq': 'on'}
        url = 'https://egrul.nalog.ru/'
        response = requests.post(url, data=data)
        response = json.loads(response.content)
        resul = requests.get('https://egrul.nalog.ru/search-result/{}'.format(response['t']))
        resp = json.loads(resul.content)

        inn_val = resp['rows'][int(nom) - 1].get('i', '0')
        region_val = resp['rows'][int(nom) - 1].get('o', '0')

        egrul_load.load_egrul_pdf(inn_val)

        for pdf_file in os.listdir(r'C:\Users\Administrator\Desktop\bot_tg_git\egr'):
            egr = pdf_file
            break

        '''nomera = self.dan.split()
                                egr = nomera[int(nom)-1]
                                strann = requests.get('https://egrul.nalog.ru/vyp-request/{}'.format(egr), stream=True)
                                filereq = requests.get('https://egrul.nalog.ru/vyp-download/{}'.format(egr), stream=True)
                                with open('egr/{}.pdf'.format(egr), "wb") as f:
                                    f.write(filereq.content)'''
        return r'C:\Users\Administrator\Desktop\bot_tg_git\egr\{}'.format(egr)
    
    def mosgor(self):
        if self.uid == '-':
            self.uid = ''
        if self.vhod == '-':
            self.vhod = ''
        if self.nom == '-':
            self.nom = ''
        if self.stor == '-':
            self.stor = ''
        session = requests.session()
        skan = ['']
        url = 'https://mos-gorsud.ru/search?formType=shortForm&courtAlias={0}&uid={1}&instance={2}&processType={3}&letterNumber={4}&caseNumber={5}&participant={6}&page=1'.format('', self.uid, '', '', self.vhod, self.nom, self.stor)
        data = session.get(url, headers=headers)
        html = bs(data.content, 'html.parser')
        i = 0
        for el in html.select('tbody'):
            q = ['']*6
            for ql in el.select('tr'):
                skan.append('')
                k = ql.select('td')
                for j in range(6):
                    q[j] = k[j].text
                    while "\n" in q[j]:
                        q[j] = q[j].replace("\n", " ")
                    while "\t" in q[j]:
                        q[j] = q[j].replace("\t", " ")
                    while "  " in q[j]:
                        q[j] = q[j].replace("  ", " ")
                if q[0] != ' ':
                    skan[i] += ' \n{}.Номер дела ~ материала: '.format(i+1)+ q[0]
                if q[1] != ' ':
                    skan[i] += ' \nСтороны: '+ q[1]
                if q[2] != ' ':
                    skan[i] += ' \nТекущее состояние: '+ q[2]
                if q[3] != ' ':
                    skan[i] += ' \nСудья: '+ q[3]
                if q[4] != ' ':
                    skan[i] += ' \nСтатья: '+ q[4]
                if q[5] != ' ':
                    skan[i] += ' \nКатегория дела: '+ q[5]
                i+=1
                if i == 10:
                    break
        stroka = ''   
        for i in skan:
            stroka += i
            
        return stroka
    
    def fssphys_zap(self):
        if self.secondname == '-':
            self.secondname = ''
        if self.birthdate == '-':
            self.birthdate = ''
        if time.time() - self.timeog < self.timehys:
            return f'Запрос неудачен, подождите ещё {(self.timeog-time.time()-self.timehys)//60} минут'
        resul = requests.get(f"https://api-ip.fssprus.ru/api/v1.0/search/physical?token={self.token}&region={self.fspreg}&firstname={self.firstname}&secondname={self.secondname}&lastname={self.lastname}&birthdate={self.birthdate}")
        resp = json.loads(resul.content)
        if resp['status'] == 'success':
            conn = sqlite3.connect(self.db_path) 
            cursor = conn.cursor()
            cursor.execute("UPDATE fspphys SET key = '{0}' WHERE id = '{1}'".format(resp['response']['task'], self.idk))
            cursor.execute("UPDATE fspphys SET time = '{0}' WHERE id = '{1}'".format(time.time(), self.idk))
            conn.commit()
            self.keyhys = resp['response']['task']
            self.timehys = time.time()
            return 'Запрос успешен'
        else:
            return 'Запрос неудачен'
        
    def fsspleg_zap(self):
        if self.address == '-':
            self.address = ''
        if time.time() - self.timeog < self.timeleg:
            return f'Запрос неудачен, подождите ещё {(self.timeog-time.time()+self.timeleg)//60} минут'
        resul = requests.get(f"https://api-ip.fssprus.ru/api/v1.0/search/legal?token={self.token}&region={self.fsplegreg}&name={self.name}&address={self.address}")
        resp = json.loads(resul.content)
        if resp['status'] == 'success':
            conn = sqlite3.connect(self.db_path) 
            cursor = conn.cursor()
            cursor.execute("UPDATE fsppleg SET key = '{0}' WHERE id = '{1}'".format(resp['response']['task'], self.idk))
            cursor.execute("UPDATE fsppleg SET time = '{0}' WHERE id = '{1}'".format(time.time(), self.idk))
            conn.commit()
            self.keyleg = resp['response']['task']
            self.timeleg = time.time()
            return 'Запрос успешен'
        else:
            return 'Запрос неудачен'

    def fsspip_zap(self):
        if time.time() - self.timeog < self.timeip:
            return f'Запрос неудачен, подождите ещё {(self.timeog-time.time()+self.timeip)//60} минут'
        resul = requests.get(f"https://api-ip.fssprus.ru/api/v1.0/search/ip?token={self.token}&number={self.numberip}")
        resp = json.loads(resul.content)
        if resp['status'] == 'success':
            conn = sqlite3.connect(self.db_path) 
            cursor = conn.cursor()
            cursor.execute("UPDATE fsppip SET key = '{0}' WHERE id = '{1}'".format(resp['response']['task'], self.idk))
            cursor.execute("UPDATE fsppip SET time = '{0}' WHERE id = '{1}'".format(time.time(), self.idk))
            conn.commit()
            self.keyip = resp['response']['task']
            self.timeip = time.time()
            return 'Запрос успешен'
        else:
            return 'Запрос неудачен'

    def fssp_prov(self, ler):
        if ler == 0:
            ler = self.keyhys
            tima = self.timehys
        elif ler == 2:
            ler = self.keyip
            tima = self.timeip
        else:
            tima = self.timeleg
            ler = self.keyleg

        while True:
            tak_status = requests.get("https://api-ip.fssprus.ru/api/v1.0/status?token={}&task={}".format(self.token, ler))
            task_status_json = json.loads(tak_status.content)
            time.sleep(3)
            if task_status_json['response']['status'] == 0:
                break
        '''
        if time.time() - self.timeog < tima:
            return f'Запрос неудачен, подождите ещё {(self.timeog-int(time.time())+tima)//60} минут'
        '''
        resul = requests.get(f"https://api-ip.fssprus.ru/api/v1.0/result?token={self.token}&task={ler}")
        resp = json.loads(resul.content)
        if resp['status'] == 'success' and resp['response']['status'] == 0:
            conn = sqlite3.connect(self.db_path) 
            cursor = conn.cursor()
            stroka = ''
            cursor.execute("UPDATE fspphys SET time = '{0}' WHERE id = '{1}'".format(time.time(),self.idk))
            cursor.execute("UPDATE fsppleg SET time = '{0}' WHERE id = '{1}'".format(time.time(),self.idk))
            cursor.execute("UPDATE fsppip SET time = '{0}' WHERE id = '{1}'".format(time.time(),self.idk))
            conn.commit()
            try:
                if resp['response']['result'][0]['result'] != []:
                    for i in resp['response']['result'][0]['result']:
                        for j in i.keys():
                            stroka += '\n'+str(i[j])
                    return stroka
                else:
                    return 'Задолженности нет'
            except Exception as e:
                return "Запрос неудачен, попробуйте снова"
        else:
            return "Запрос неудачен, попробуйте сделать новый поиск"
