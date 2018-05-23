import requests
import json
import time
import hashlib
import pymysql
from ignore import db_config as config


class ZshCrawler:
    get_login_url = 'http://www.sinopecsales.com/websso/loginAction_form.action'
    v_code_url = 'http://www.sinopecsales.com/websso/YanZhengMaServlet'
    post_login_url = 'http://www.sinopecsales.com/websso/loginAction_login.json'
    user_basic_info_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryBalance.json'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.sinopecsales.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    headers2 = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.sinopecsales.com',
        'Origin': 'http://www.sinopecsales.com',
        'Referer': 'http://www.sinopecsales.com/gas/webjsp/query/billDetail.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    login_cookie = ''

    @staticmethod
    def __connect_db():
        try:
            db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                                 passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
            return db
        except:
            return False

    @staticmethod
    def __connect_db2():
        try:
            db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                                 passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
            return db
        except:
            return False

    def get_account_and_pwd_from_db(self, id=None):
        db = self.__connect_db2()
        cursor = db.cursor()
        sql = 'SELECT `login_name`,`login_pwd` FROM st_oilcard_userinfo WHERE state_now = 4 AND charge_type=1 ORDER BY RAND() LIMIT 1'
        # sql = "SELECT login_name,login_pwd FROM st_oilcard_userinfo WHERE  state_now = 4 AND charge_type=1";
        # if id is None:
        #     sql = ""
        # else:
        #     sql = ""

        try:
            cursor.execute(sql)
            info = cursor.fetchone()
            return info
        except:
            return False

    def set_login_cookie(self, login_cookie):
        self.login_cookie = login_cookie
        return self

    def get_login_cookie(self):
        return self.login_cookie

    def simulate_login(self):
        """
        模拟登陆
        :return: bool
        """
        # account_info = self.get_account_and_pwd_from_db()
        # if not account_info:
        #     print('get account from db failed.....')
        #     exit()
        try:
            cookie = requests.get(self.get_login_url, headers=self.headers).cookies
            v_code = requests.get(self.v_code_url, headers=self.headers, cookies=cookie).content
            with open('aa.jpeg', 'wb') as fd:
                fd.write(v_code)
                fd.close()
            v_code2 = input('please enter your v_code:')
            post_data = {
                # 'memberAccount': 'Uc865a2df1ae27731',
                # 'memberUmm': hashlib.sha1('Uc355a2d'.encode('utf-8')).hexdigest(),
                'memberAccount': 'youka66666',
                'memberUmm': hashlib.sha1('abcd123@'.encode('utf-8')).hexdigest(),
                'check': v_code2,
                'rememberMe': 'on'
            }
            login = requests.post(self.post_login_url, data=post_data, cookies=cookie)
            if json.loads(login.text)['success'] == 0:
                self.set_login_cookie(login.cookies)
                print('logging successfully!!!!!!')
                return True
        except Exception as e:
            raise Exception('login failed.......... '+str(e))

    def scrape_oil_card(self, cookie):
        target_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryBalance.json'
        try:
            text = requests.get(target_url, headers=self.headers, cookies=cookie).text
            return json.loads(text)['cardInfo']['cardNo']
        except:
            return False

    def scrape_top_up_detail(self, time_start, time_end, card_no):
        target_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_chargeDetail.json'
        form_data = {
            'cardMember.cardNo': card_no,
            'startTime': time_start,
            'endTime': time_end
        }
        try:
            text = requests.post(target_url, data=form_data, headers=self.headers2,
                                 cookies=self.get_login_cookie()).text
            return text
        except:
            return False

    def insert_data_to_db(self):
        pass

    def scrape_trade_detail_by_month(self, cookie, time_start, card_no):
        """
        通过月份来爬取交易明细
        :param cookie:
        :param time_start:
        :param card_no:
        :return:
        """
        default_cookie = cookie
        target_url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_getCardInfoObject.json'
        target_url2 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryViceCardList.json'
        target_url3 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_transactionLog.json'
        form_data1 = {'cardMember.cardNo': card_no}
        form_data2 = {'cardMember.cardNo': card_no, 'cardsType': -1, 'lastCardNo': ''}
        form_data4 = {
            'cardMember.cardNo': card_no,
            'startTime': time_start,
            'endTime': '',
            'traType': None,
            'dateFlag': None
        }
        try:
            # print(default_cookie)
            res1 = requests.post(target_url1, data=form_data1, headers=self.headers2, cookies=default_cookie)
            text1 = res1.text
            default_cookie.pop('yunsuo_session_verify')
            default_cookie.set('yunsuo_session_verify', res1.cookies.get('yunsuo_session_verify'),
                               domain='www.sinopecsales.com', path='/')
            print(text1)
            # print(default_cookie)
            res2 = requests.post(target_url2, data=form_data2, headers=self.headers2, cookies=default_cookie)
            text2 = res2.text
            default_cookie.pop('yunsuo_session_verify')
            default_cookie.set('yunsuo_session_verify', res2.cookies.get('yunsuo_session_verify'),
                               domain='www.sinopecsales.com', path='/')
            print(text2)
            # print(default_cookie)
            form_data3 = {
                'cardMember.cardNo': card_no,
                'cardsType': -1,
                'lastCardNo': json.loads(text2)['lastCardNo']
            }
            res3 = requests.post(target_url2, data=form_data3, headers=self.headers2, cookies=default_cookie)
            text3 = res3.text
            default_cookie.pop('yunsuo_session_verify')
            default_cookie.set('yunsuo_session_verify', res3.cookies.get('yunsuo_session_verify'),
                               domain='www.sinopecsales.com', path='/')
            print(text3)
            # print(default_cookie)
            print('waiting......')
            time.sleep(1)
            time_stamp = str(time.time())[:14].replace('.', '')
            text4 = requests.post(target_url3 + '?sjs=' + time_stamp, data=form_data4, headers=self.headers2,
                                  cookies=default_cookie).text
            print(text4)
            return text4
        except:
            return False

    def action(self):
        # data = self.get_account_and_pwd_from_db()
        # print(data)
        # exit()
        # 模拟登陆
        login_res = self.simulate_login()
        if not login_res:
            print('login failed......')
            exit()
        # 获取该账户的卡号
        card = self.scrape_oil_card(self.get_login_cookie())
        if not card:
            print('scrape card no failed......')
            exit()
        # 获取交易信息
        trade_detail = self.scrape_trade_detail_by_month(self.get_login_cookie(), '2017-12', card)

        # 获取充值明细
        # top_up_detail = self.scrape_top_up_detail('2017-12-1', '2017-12-21', card)
        # print(top_up_detail)


crawler = ZshCrawler()
crawler.action()
# print(hashlib.sha1('Uc355a2d'.encode('utf-8')).hexdigest())
