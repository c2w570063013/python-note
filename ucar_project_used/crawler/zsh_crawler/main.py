import requests
import hashlib
import json
import pymysql
import datetime
import dateutil.relativedelta as date_process
from zsh_crawler import v_code_idetify as v_code_
import base64
from ignore import db_config as config


class Crawler:
    v_code_url = 'http://www.sinopecsales.com/websso/YanZhengMaServlet'
    post_login_url = 'http://www.sinopecsales.com/websso/loginAction_login.json'
    user_basic_info_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryBalance.json'
    card_no_info = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryBalance.json'
    # 交易明细明细相关目标连接
    trade_detail_url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_getCardInfoObject.json'
    trade_detail_url2 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryViceCardList.json'
    trade_detail_url3 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_transactionLog.json'
    # 充值明细 目标连接
    top_up_detail = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_chargeDetail.json'

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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    card_no = ''

    def __init__(self):
        self.s = requests.session()

    @staticmethod
    def __connect_db2():
        """
        链接数据库
        :return:
        """
        try:
            db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                                 passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
            return db
        except Exception as e:
            print(e)
            exit()

    def simulate_login(self, n=5):
        i = 0
        while i < n:
            print('正在获取验证码.............')
            v_code_content = self.s.get(self.v_code_url, headers=self.headers).content
            base_64_content = base64.b64encode(v_code_content)
            print('正在识别验证码.............')
            v_code_o = v_code_.IdentifyVCode(base_64_content)
            v_code2 = v_code_o.return_identify_res()
            post_data = {
                # 'memberAccount': 'Ucar_123',
                # 'memberUmm': hashlib.sha1('cai123456'.encode('utf-8')).hexdigest(),
                # 'memberAccount': 'Uc865a2df1ae27731',
                # 'memberUmm': hashlib.sha1('Uc355a2d'.encode('utf-8')).hexdigest(),
                'memberAccount': 'youka66666',
                'memberUmm': hashlib.sha1('abcd123@'.encode('utf-8')).hexdigest(),
                'check': v_code2,
                'rememberMe': 'on'
            }
            print('验证码识别成功，开始尝试登陆..........')
            login = self.s.post(self.post_login_url, headers=self.headers, data=post_data)
            if json.loads(login.text)['success'] == 0:
                print('登陆成功!!!!!!!!!!')
                break
            i += 1

    # def test(self):
    #     text = self.s.get(self.card_no_info, headers=self.headers).text
    #     print(text)

    def scrape_oil_card(self):
        try:
            print('正在获取用户油卡卡号......')
            text = self.s.get(self.card_no_info, headers=self.headers).text
            self.card_no = json.loads(text)['cardInfo']['cardNo']
            print('ok..')
        except Exception as e:
            print(e)
            exit()

    def scrape_trade_detail(self):
        print('正在获取油卡交易详情')
        try:
            form1 = {'cardMember.cardNo': self.card_no}
            x1 = self.s.post(self.trade_detail_url1, data=form1, headers=self.headers2).text
            print(x1)
            form2 = {'cardMember.cardNo': self.card_no, 'startTime': '2018-01', 'traType': False, 'dateFlag': False}
            x2 = self.s.post(self.trade_detail_url3, data=form2, headers=self.headers2).text
            print(x2)

        except Exception as e:
            print(e)
            exit()

    def action(self):
        self.simulate_login()
        self.scrape_oil_card()
        self.scrape_trade_detail()


crawler = Crawler()
crawler.action()
