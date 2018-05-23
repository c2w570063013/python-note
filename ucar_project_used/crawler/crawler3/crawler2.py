import requests
import json
import time
from http.cookies import BaseCookie
from bs4 import BeautifulSoup
import xlrd
import shutil
import xlsxwriter
import pandas as pd
import hashlib


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    card_no = 1000114400020153262
    # post
    target_url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_getCardInfoObject.json'
    target_url2 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryViceCardList.json'
    target_url3 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_transactionLog.json'

    def simulate_login(self):
        cookie = requests.get(self.get_login_url, headers=self.headers).cookies
        v_code = requests.get(self.v_code_url, headers=self.headers, cookies=cookie).content
        with open('aa.jpeg', 'wb') as fd:
            fd.write(v_code)
            fd.close()
        v_code2 = input('please enter your v_code:')

        post_data = {
            'memberAccount': 'Uc865a2df1ae27731',
            'memberUmm': hashlib.sha1('Uc355a2d'.encode('utf-8')).hexdigest(),
            'check': v_code2,
            'rememberMe': 'on'
        }
        login = requests.post(self.post_login_url, data=post_data, cookies=cookie)
        if json.loads(login.text)['success'] == 0:
            return login.cookies

        return False

    def scrape_data(self):
        login_cookie = self.simulate_login()

        if login_cookie is False:
            print('logging failed!!!')
            exit()
        form_data1 = {'cardMember.cardNo': self.card_no}
        # print(login_cookie)
        request1 = requests.post(self.target_url1, data=form_data1, cookies=login_cookie, headers=self.headers2)
        print(request1.text)
        # print(request1.cookies)

        login_cookie.pop('yunsuo_session_verify')
        login_cookie.set('yunsuo_session_verify', request1.cookies.get('yunsuo_session_verify'),
                         domain='www.sinopecsales.com')

        form_data2 = {'cardMember.cardNo': self.card_no, 'cardsType': -1}
        request2 = requests.post(self.target_url2, cookies=login_cookie, headers=self.headers2, data=form_data2)
        print(request2.text)

        login_cookie.pop('yunsuo_session_verify')
        login_cookie.set('yunsuo_session_verify', request2.cookies.get('yunsuo_session_verify'),
                         domain='www.sinopecsales.com')

        requests3 = requests.post(self.target_url2, cookies=login_cookie, headers=self.headers2,
                                  data={'cardMember.cardNo': self.card_no, 'cardsType': -1,
                                        'lastCardNo': 1000114400020153310})
        print(requests3.text)

        card_list = json.loads(request2.text)

        form_data4 = {'cardMember.cardNo': '', 'startTime': '2017-12-14', 'endTime': '2017-12-14', 'traType': 'false',
                      'dateFlag': 'true'}
        # print(card_list['list'])
        # exit()
        for i in card_list['list']:
            print('------------------------------------------------------------')
            # print(cookie_list[0])
            form_data4['cardMember.cardNo'] = i['cardNo']
            url_ = self.target_url3 + '?sjs' + str(time.time())[:14].replace('.', '')
            requests4 = requests.post(url_, headers=self.headers2, data=form_data4, cookies=login_cookie)
            # print(requests4.cookies.get('yunsuo_session_verify'))

            print(requests4.text)
            # print('------------------------------------------------------------')
        exit()

    def scrape_data2(self):
        login_cookie = self.simulate_login()
        if login_cookie is False:
            print('logging failed!!!')
            exit()
        url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_getCardInfoObject.json'
        url2 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_balanceCardList.json'
        url_header_refer = 'http://www.sinopecsales.com/gas/webjsp/query/balance.jsp'
        self.headers2['Referer'] = url_header_refer
        form_data1 = {'cardMember.cardNo': 1000114400020153262}
        res1 = requests.post(url1, data=form_data1, headers=self.headers2, cookies=login_cookie)
        print(res1.text)

        form_data2 = {'cardMember.cardNo': 1000114400020153262, 'cardNum': 0}
        res2 = requests.post(url2, data=form_data2, headers=self.headers2, cookies=login_cookie)
        print(res2.text)

    def scrape_data3(self):
        login_cookie = self.simulate_login()
        if login_cookie is False:
            print('logging failed!!!')
            exit()
        # url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryFile.json'
        # form = {'fid': 201712140950185827}
        # res = requests.post(url, data=form, headers=self.headers2, cookies=login_cookie)
        # print(res.text)

        xx = requests.get(
            'http://www.sinopecsales.com/gas/webjsp/billQueryAction_excelOutPut.action?fid=201712140950185827',
            headers=self.headers, cookies=login_cookie, stream=True)

        # file = 'test.xls'
        # output = open(file, 'wb')
        # output.write(xx.content)
        # output.close()
        workbook = xlrd.open_workbook(file_contents=xx.content)
        worksheet = workbook.sheet_by_index(0)
        print(worksheet.cell(0, 0).value)
        print(worksheet.nrows)
        print(worksheet.ncols)

    def scrape_card_info(self):
        """
        抓取卡信息
        :return:
        """
        login_cookie = self.simulate_login()
        if login_cookie is False:
            print('logging failed!!!')
            exit()
        print('logging successfully')
        url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryViceCardList2.json'
        form_data1 = {'cardMember.cardNo': 1000114400020153262, 'cardsType': -1}
        res1 = requests.post(url1, data=form_data1, headers=self.headers, cookies=login_cookie)
        print(res1.text)
        list_1 = json.loads(res1.text)

        url2 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryCardHolder.json'
        for i in list_1['list']:
            form_data2 = {'holderCardNo': i['cardNo'], 'priCardNo': '1000114400020153262'}
            res2 = requests.post(url2, data=form_data2, headers=self.headers, cookies=login_cookie)
            print(res2.text)

    def scrape_trade_detail(self):
        login_cookie = self.simulate_login()
        if login_cookie is False:
            print(bcolors.FAIL + 'logging failed!!!' + bcolors.ENDC)
            exit()
        print(bcolors.OKGREEN + 'logging successfully!!!' + bcolors.ENDC)
        url1 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_transactionDetailsExcel.json'
        url2 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_queryDownLoadList.json'
        url3 = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_removeExcel.json'
        down_load_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_excelOutPut.action'
        form_data1 = {'cardMember.cardNo': self.card_no, 'startTime': '2017-12-14', 'endTime': '2017-12-14',
                      'traType': 'false', 'cardsType': -1, 'dateFlag': 'true'}

        res1 = requests.post(url1, data=form_data1, headers=self.headers, cookies=login_cookie)
        print(res1.text)
        print('waiting for download the excel file...for 5 seconds......')
        time.sleep(5)
        while True:
            res2 = requests.post(url2, data={'cardMember.cardNo': 1000114400020153262}, headers=self.headers,
                                 cookies=login_cookie)
            res2_dic = json.loads(res2.text)
            print(res2_dic)
            # the download list is ordered by asc not desc
            if int(res2_dic['list'][len(res2_dic['list']) - 1]['status']) == 1:
                # obtain trade record and save to file
                content = requests.get(down_load_url + '?fid=' + res2_dic['list'][0]['fid'], headers=self.headers,
                                       cookies=login_cookie).content
                output = open('test1.xls', 'wb')
                output.write(content)
                # remove the excel generated by the previous operation
                requests.post(url3, headers=self.headers, cookies=login_cookie,
                              data={'fid': res2_dic['list'][0]['fid']})
                break
            print('waiting 10 seconds again for downloading the excel file......')
            time.sleep(10)

        print(bcolors.OKGREEN + 'done!!!!!!!!!!!!!!!!!!!!' + bcolors.ENDC)

    def scrape_top_up_detail(self):
        login_cookie = self.simulate_login()
        if login_cookie is False:
            print(bcolors.FAIL + 'logging failed!!!' + bcolors.ENDC)
            exit()
        print(bcolors.OKGREEN + 'logging successfully!!!' + bcolors.ENDC)
        request_url = 'http://www.sinopecsales.com/gas/webjsp/billQueryAction_chargeDetail.json'
        form_data = {
            'cardMember.cardNo': 1000113300009176795,
            'startTime': '2017-10-01',
            'endTime': '2017-12-19'
        }
        res = requests.post(request_url, data=form_data, headers=self.headers, cookies=login_cookie)
        print(res.text)

    @staticmethod
    def __parse_excel(excel_content):
        workbook = xlrd.open_workbook(file_contents=excel_content)
        worksheet = workbook.sheet_by_index(0)
        rows = worksheet.nrows
        cols = worksheet.ncols
        return [rows, cols]


crawler = ZshCrawler()
crawler.scrape_top_up_detail()
# print(bcolors.OKGREEN + 'i am testing differences colors......' + bcolors.ENDC)
# print(bcolors.FAIL + 'i am testing differences colors......' + bcolors.ENDC)
# print(bcolors.WARNING + 'i am testing differences colors......' + bcolors.ENDC)
# print(bcolors.BOLD + 'i am testing differences colors......' + bcolors.ENDC)
# print(bcolors.HEADER + 'i am testing differences colors......' + bcolors.ENDC)
# print(bcolors.OKBLUE + 'i am testing differences colors......' + bcolors.ENDC)
