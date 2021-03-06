import requests
import hashlib
import json
import pymysql
import datetime
import dateutil.relativedelta as date_process
from v_code import v_code_idetify as v_code_
import base64
from ignore import db_config as config

class Crawler:
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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    card_no = ''

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

    def simulate_login2(self, session, n=5):
        """
        模拟登陆
        :param session:
        :param n:最多有n次错误机会
        :return:
        """
        i = 0
        while i < n:
            print('正在获取验证码..........')
            v_code_content = session.get(self.v_code_url, headers=self.headers).content
            base_64_content = base64.b64encode(v_code_content)
            print('正在识别验证码.............')
            v_code_o = v_code_.IdentifyVCode(base_64_content)
            v_code2 = v_code_o.return_identify_res()
            # 如果识别验证码失败 重新调用借口进行识别
            if not v_code2:
                continue
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
            login = session.post(self.post_login_url, headers=self.headers, data=post_data)
            if json.loads(login.text)['success'] == 0:
                print('登陆成功!!!!!!!!!!')
                break
            i += 1

    def set_card_no(self, card_no):
        self.card_no = card_no
        return self

    def scrape_oil_card(self, session):
        """
        获取账号的油卡信息
        :param session:
        :return:
        """
        target_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryBalance.json'
        try:
            text = session.get(target_url, headers=self.headers).text
            self.set_card_no(json.loads(text)['cardInfo']['cardNo'])
            # return json.loads(text)['cardInfo']['cardNo']
        except Exception as e:
            print('suck me')
            print(e)
            exit()

    def scrape_top_up_detail(self, session, start_time, end_time):
        """
        爬取充值明细信息
        :param session:
        :param start_time:
        :param end_time:
        :return:
        """
        target_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_chargeDetail.json'
        form_data = {
            'cardMember.cardNo': self.card_no,
            'startTime': start_time,
            'endTime': end_time
        }
        print('发送请求 获取充值明细数据......')
        res = session.post(target_url, data=form_data, headers=self.headers2).text
        res_dic = json.loads(res)
        db = self.__connect_db2()
        cursor = db.cursor()
        print('正在将充值明细 保存进数据库中......')
        for i in res_dic['list']:
            amount = str(int(i['amount']) / 100 if int(i['amount']) != 0 else 0)
            insert_sql = "INSERT INTO `la_zsh_top_up_detail` (`location`,`oil_card`,`receipt_type`,`top_up_amount`,`trade_time`,`created_at`) VALUES ('%s','%s','%s','%s','%s',now())" % (
                i['nodeTag'], self.card_no, i['advpayType'], amount, i['opeTime'])
            try:
                cursor.execute(insert_sql)
                db.commit()
            except Exception as e:
                print(e)
                exit()

    def scrape_trade_detail_by_month2(self, session, months):
        """
        通过月份爬取交易信息
        :param session: str
        :param months: list
        :return:
        """
        form1 = {'cardMember.cardNo': self.card_no}
        url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_getCardInfoObject.json'
        print('正在模拟发送查询卡信息请求...........')
        session.post(url1, data=form1, headers=self.headers2)
        form4 = {'cardMember.cardNo': self.card_no, 'startTime': '', 'traType': False, 'dateFlag': False}
        url4 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_transactionLog.json'

        for month in months:
            form4['startTime'] = month
            print('根据' + str(month) + '月份查询卡交易信息......')
            res4 = session.post(url4, data=form4, headers=self.headers2).text
            res4_dic = json.loads(res4)
            # 持卡人
            holders = res4_dic['holders']
            card_no = res4_dic['no']
            db = self.__connect_db2()
            cursor = db.cursor()
            print('正在插入' + str(month) + '月份数据到数据库!--------------------------------')
            # 如果为空则跳过
            if not res4_dic['list']:
                continue
            for i in res4_dic['list']:
                # 交易金额
                amount = str(int(i['amount']) / 100 if int(i['amount']) != 0 else 0)
                # 加油数量
                liter = str(int(i['litre']) / 100 if int(i['litre']) != 0 else 0)
                # 单价
                price = str(int(i['price']) / 100 if int(i['price']) != 0 else 0)
                # 奖励积分
                reward = str(i['reward'] / 100 if int(i['reward']) != 0 else 0)
                # 余额
                balance = str(int(i['balance']) / 100 if int(i['balance']) != 0 else 0)
                # 插入时间
                now_ = str(datetime.datetime.today())[:19]
                # 插入数据sql
                insert_sql = "INSERT INTO `la_zsh_trade_detail` (`card_no`,`card_owner`,`trade_time`,`trade_type`,`amount`,`oil_type`,`oil_num`,`price`,`reward_point`,`balance`,`location`,`created_at`) VALUES ('" + str(
                    card_no) + "','" + holders + "','" + i['opeTime'] + "','" + i['traName'] + "'," + amount + ",'" + i[
                                 'oilName'] + "'," + liter + "," + price + "," + reward + "," + balance + ",'" + i[
                                 'nodeTag'] + "','" + now_ + "')"
                try:
                    cursor.execute(insert_sql)
                    db.commit()
                except Exception as e:
                    print('fuck u')
                    print(e)
                    exit()

    def scrape_trade_detail_in_main_card_by_month(self, session, month):
        url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_getCardInfoObject.json'
        url2 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryViceCardList.json'
        url3 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_transactionLog.json'
        form1 = {'cardMember.cardNo': self.card_no}
        form2 = {'cardMember.cardNo': self.card_no, 'cardsType': -1}
        form3 = {'cardMember.cardNo': self.card_no, 'startTime': month, 'traType': False, 'dateFlag': False}
        res1 = session.post(url1, data=form1, headers=self.headers2).text
        print(res1)
        res2 = session.post(url2, data=form2, headers=self.headers2).text
        res2_dic = json.loads(res2)
        print('------------------------------------------------------------------------------------------')
        for i in res2_dic['list']:
            form3['cardMember.cardNo'] = i['cardNo']
            res3 = session.post(url3, data=form3, headers=self.headers2).text
            print(res3)
        pass

    @staticmethod
    def process_recent_months(date, n=3):
        """
        产生最近的月份
        :param date:
        :param n:
        :return:
        """
        tmp_date_list = [date]
        tmp_year_month_list = [str(date)[:7]]
        for i in range(n):
            tmp_d = tmp_date_list[0] - date_process.relativedelta(months=1)
            tmp_date_list.pop()
            tmp_date_list.append(tmp_d)
            tmp_year_month_list.append(str(tmp_d)[:7])
        del tmp_date_list
        return tmp_year_month_list

    def main_action2(self):
        # 创建session
        s = requests.session()
        # 模拟登陆
        self.simulate_login2(s)
        # 获取账号油卡
        self.scrape_oil_card(s)
        # 产生最近4个月的时间
        months_list = self.process_recent_months(datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'))
        # 爬取交易信息
        self.scrape_trade_detail_by_month2(s, months_list)
        # 爬取充值明细
        # self.scrape_top_up_detail(s, '2017-10-01', '2018-01-06')
        print('done!!!!!!!!!!!!!!!!!!!')


crawler = Crawler()
crawler.main_action2()
