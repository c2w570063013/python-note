import crawler2.identify_v_code as identify_v_code
import datetime
import requests
import base64
from bs4 import BeautifulSoup
import re
import pymysql
import inspect
from ignore import db_config


class Crawler:
    login_url = 'http://card.bppc.com.cn/weblogin.aspx'

    v_code_url = 'http://card.bppc.com.cn/IdentifyCode.aspx'

    consumed_url = 'http://card.bppc.com.cn/WebConsumeDetail.aspx'

    top_up_url = 'http://card.bppc.com.cn/WebPayDetail.aspx'

    __error_log = 'error.log'

    __login_post_data = {
        'ctl00$ContentPlaceHolder1$txtID': '50042742',
        'ctl00$ContentPlaceHolder1$txtPWD': 'ucar99882016',
        'ctl00$ContentPlaceHolder1$txtCheck': '',
        '__VIEWSTATE': '/wEPDwUKMTQxMDQ4NDAyMmRkobdBOsFxX2WDVDhsoxI9GxIOTLw=',
        'ctl00$ContentPlaceHolder1$btnLogin': '50042742'
    }

    def __init__(self, time_start='', time_end=''):
        if time_start == '':
            self.time_start = datetime.date.today() - datetime.timedelta(1)
        else:
            self.time_start = time_start

        if time_end == '':
            self.time_end = datetime.date.today() - datetime.timedelta(1)
        else:
            self.time_end = time_end
        print('get cookies from url......')
        self.cookie = requests.get(self.login_url).cookies

    def simulate_login(self, login_times=5):
        for i in range(login_times):
            # instantiate IdentifyCode
            identify_ = identify_v_code.IdentifyCode()
            print('get v_code from url')
            v_code_base_64_img = base64.b64encode(requests.get(self.v_code_url, cookies=self.cookie).content)
            # print(v_code_base_64_img)
            # exit()
            print('identifying v_code......')
            check_v_res = identify_.identify_v_code(v_code_base_64_img)
            # if identify v code failed
            if not check_v_res:
                with open(self.get_error_log(), 'a', encoding='utf-8') as f:
                    f.write('验证码识别错误 ' + str(datetime.datetime.today())[:19] + '\n')
                    f.close()
                    continue
            self.__login_post_data['ctl00$ContentPlaceHolder1$txtCheck'] = check_v_res
            print('attempting logging......')
            login_res = requests.post(self.login_url, data=self.__login_post_data, cookies=self.cookie)
            if login_res.status_code == 200 and 'WebAccountDetail.aspx' in login_res.text.encode('ascii', 'ignore') \
                    .decode('utf-8'):
                break
            if i == login_times - 1:
                with open(self.get_error_log(), 'a', encoding='utf-8') as f:
                    f.write('屡次尝试登陆失败 ' + str(datetime.datetime.today())[:19] + '\n')
                    f.close()
                    exit()
            print('try logging again!!!!!!')

        print('logging successfully!!!!!!')
        return True

    def get_default_page_view_tag(self, target_url):
        """
        get default page view tag
        :param target_url:
        :return: view_tag
        """
        default_page = requests.get(target_url, cookies=self.cookie)
        if default_page.status_code != 200:
            with open(self.get_error_log(), 'a', encoding='utf-8') as f:
                f.write('获取登陆之后首页失败 ' + inspect.currentframe().f_code.co_filename + ' 第' +
                        inspect.currentframe().f_lineno + '行' +
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
                f.close()
                exit()
        return BeautifulSoup(default_page.text, 'html.parser').find('input', {'id': '__VIEWSTATE'}).get('value')

    def get_first_page_info_and_save_it_and_get_main_info_filtered_by_date(self, view_tag, target_url,
                                                                           consumed_or_top_up):
        post_data2 = {
            'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$updatepannel1|ctl00$ContentPlaceHolder1$btnSearch',
            '__VIEWSTATE': view_tag,
            'ctl00$ContentPlaceHolder1$ddlDateType': 1,
            'ctl00$ContentPlaceHolder1$ddlShift': 0,
            'ctl00$ContentPlaceHolder1$btnSearch': '查询',
            'ctl00$ContentPlaceHolder1$txtDate1': self.time_start,
            'ctl00$ContentPlaceHolder1$txtDate2': self.time_end
        }

        # 获取使用日期筛选 之后的第一页 页面
        print('obtaining the first page of filtered data by date......')
        filter_data_page = requests.post(target_url, data=post_data2, cookies=self.cookie)
        if filter_data_page.status_code == 200:
            soup = BeautifulSoup(filter_data_page.text, 'html.parser')
            page_info = soup.select('span#ctl00_ContentPlaceHolder1_lblinfo')[0].text
            page_info_num = re.findall('\d+', page_info)
            # 如果条数为0 则退出
            if int(page_info_num[0]) == 0:
                return None
            # 总页数
            total_pages = int(page_info_num[1])
            # 将第一页数据解析并插入至数据库中
            print('parse 1 page dom and save data to db......')
            self.parse_dom_and_save_data_to_db(filter_data_page.text, consumed_or_top_up)
            # 如果只有一页数据 则退出
            if total_pages == 1:
                return None
            # 获取该页面的 标识符
            default_view2 = soup.find('input', {'id': '__VIEWSTATE'}).get('value')
            return {'total_pages': total_pages, "default_view": default_view2}
        else:
            print('error...........')
            with open(self.__error_log, 'a', encoding='utf-8') as f:
                f.write('获取页面失败' + inspect.currentframe().f_code.co_filename + ' 第' +
                        inspect.currentframe().f_lineno + '行' +
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
                f.close()
            exit()

    @staticmethod
    def __connect_db():
        db = pymysql.connect(host=db_config.db_config['host'], port=db_config.db_config['port'], user=db_config.db_config['user'],
                             passwd=db_config.db_config['pwd'], db=db_config.db_config['db'], charset='utf8')
        return db

    def parse_dom_and_save_data_to_db(self, html_content, consumed_or_to_up=1):
        html = BeautifulSoup(html_content, 'html.parser')
        table = html.find('table', {'id': 'ctl00_ContentPlaceHolder1_tbNews'})
        tr = table.findAll('tr')
        db = self.__connect_db()
        cursor = db.cursor()

        tmp_val_list = []
        for i in tr[1:]:
            td = i.findAll('td')
            # 如果是消费详情 则不需要状态
            for j in td[1:] if consumed_or_to_up == 1 else td:
                span_val = j.find('span').text
                tmp_val_list.append(span_val)

            date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if consumed_or_to_up == 1:
                oil = re.findall('\d+', tmp_val_list[3])
                oil_type = 'NULL'
                if len(oil) > 0:
                    oil_type = oil[0]
                insert_sql = "INSERT INTO la_bp_consumed_detail (account,oil_card_num,petrol_station,consumed_item,petrol_price,discount_price,consumed_price,after_discount_price,consumed_amount,car_id_num,consumed_time,oil_type,created_at) " \
                             "VALUES (" + tmp_val_list[0] + "," + tmp_val_list[1] + ",'" + tmp_val_list[2] + "','" + \
                             tmp_val_list[3] + "'," + tmp_val_list[4] + "," + tmp_val_list[5] + "," + tmp_val_list[
                                 6] + "," + tmp_val_list[7] + "," + tmp_val_list[8] + ",'" + tmp_val_list[9] + "','" + \
                             tmp_val_list[10] + "'," + oil_type + ",'" + date_now + "')"
            else:
                oil_card_num = tmp_val_list[2] if tmp_val_list[2] else 'NULL'
                insert_sql = "INSERT INTO la_bp_top_up_detail (top_up_site,main_account,oil_card_num,charge_amount,charge_type,charge_time,created_at) VALUES ('" + \
                             tmp_val_list[0] + "','" + tmp_val_list[1] + "'," + oil_card_num + ",'" + tmp_val_list[
                                 3] + "','" + tmp_val_list[4] + "','" + tmp_val_list[5] + "','" + date_now + "')"
            try:
                cursor.execute(insert_sql)
                db.commit()
            except:
                with open('error.log', 'a', encoding='utf-8') as f:
                    f.write('插入错误 ' + insert_sql + '  ' + date_now)
                db.rollback()
            del tmp_val_list
            tmp_val_list = []
        db.close()

    def loop_all_page_and_get_data(self, default_view, target_url, total_pages, consumed_or_top_up):
        post_data = {
            'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$updatepannel2|ctl00$ContentPlaceHolder1$btnnext',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btnnext',
            '__VIEWSTATE': '',
            'ctl00$ContentPlaceHolder1$txtDate1': self.time_start,
            'ctl00$ContentPlaceHolder1$txtDate2': self.time_end
        }
        view_state_list = [default_view]
        for i in range(total_pages - 1):
            print('parse ' + str(i + 2) + ' page dom and save to db......')
            post_data['__VIEWSTATE'] = view_state_list[0]
            del view_state_list
            view_state_list = []
            res = requests.post(target_url, data=post_data, cookies=self.cookie)
            if res.status_code == 200:
                self.parse_dom_and_save_data_to_db(res.text, consumed_or_top_up)

            view_state = BeautifulSoup(res.text, 'html.parser').find('input', {'id': '__VIEWSTATE'}).get('value')
            view_state_list.append(view_state)

        del view_state_list
        del post_data

    def start_crawling(self, target_url, consumed_or_top_up):
        view_tag = self.get_default_page_view_tag(target_url)
        data = self.get_first_page_info_and_save_it_and_get_main_info_filtered_by_date(view_tag, target_url,
                                                                                       consumed_or_top_up)
        if data is not None:
            self.loop_all_page_and_get_data(data['default_view'], target_url, data['total_pages'],
                                            consumed_or_top_up)

    def action(self):
        login_res = self.simulate_login()
        if login_res:
            self.start_crawling(self.consumed_url, 1)
            self.start_crawling(self.top_up_url, 2)

    def set_error_log(self, file):
        self.__error_log = file

    def get_error_log(self):
        return self.__error_log


crawler = Crawler()
crawler.action()
