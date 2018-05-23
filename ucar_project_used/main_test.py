import base64
import datetime

import requests
from bs4 import BeautifulSoup

from ucar_project_used.identify_v_code import IdentifyCode


class Crawler:
    login_url = 'http://card.bppc.com.cn/weblogin.aspx'

    v_code_url = 'http://card.bppc.com.cn/IdentifyCode.aspx'

    consumed_url = 'http://card.bppc.com.cn/WebConsumeDetail.aspx'

    top_up_url = 'http://card.bppc.com.cn/WebPayDetail.aspx'

    time_start = datetime.date.today() - datetime.timedelta(1)

    time_end = datetime.date.today() - datetime.timedelta(1)

    __error_log = 'error.log'

    __login_post_data = {
        'ctl00$ContentPlaceHolder1$txtID': '50042742',
        'ctl00$ContentPlaceHolder1$txtPWD': 'ucar99882016',
        'ctl00$ContentPlaceHolder1$txtCheck': '',
        '__VIEWSTATE': '/wEPDwUKMTQxMDQ4NDAyMmRkobdBOsFxX2WDVDhsoxI9GxIOTLw=',
        'ctl00$ContentPlaceHolder1$btnLogin': '50042742'
    }

    __common_post_data = {
        'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$updatepannel1|ctl00$ContentPlaceHolder1$btnSearch',
        '__VIEWSTATE': '',
        'ctl00$ContentPlaceHolder1$ddlDateType': 1,
        'ctl00$ContentPlaceHolder1$ddlShift': 0,
        'ctl00$ContentPlaceHolder1$txtDate1': '',
        'ctl00$ContentPlaceHolder1$txtDate2': ''
    }

    def __init__(self):
        self.cookie = requests.get(self.login_url).cookies

    def simulate_login(self, login_times=5):
        for i in range(login_times):
            # get v_code from url
            v_code_base_64_img = base64.b64encode(requests.get(self.v_code_url, cookies=self.cookie).content)
            check_v_res = IdentifyCode.identify_v_code(v_code_base_64_img)
            # if identify v code failed
            if not check_v_res:
                with open(self.get_error_log(), 'a', encoding='utf-8') as f:
                    f.write('验证码识别错误 ' + str(datetime.datetime.today())[:19] + '\n')
                    f.close()
                    exit()
            self.__login_post_data['ctl00$ContentPlaceHolder1$txtCheck'] = v_code_base_64_img
            # attempt logging
            login_res = requests.post(self.login_url, data=self.__login_post_data, cookies=self.cookie)
            if login_res.status_code == 200:
                # logging successfully
                break
            if i == login_times - 1:
                with open(self.get_error_log(), 'a', encoding='utf-8') as f:
                    f.write('屡次尝试登陆失败 ' + str(datetime.datetime.today())[:19] + '\n')
                    f.close()
                    exit()
        return True

    def get_default_page_view_tag(self, target_url):
        """
        get default page view tag
        :param target_url:
        :return:
        """
        default_page = requests.get(target_url, cookies=self.cookie)
        if default_page.status_code != 200:
            with open(self.get_error_log(), 'a', encoding='utf-8') as f:
                f.write('获取登陆之后首页失败 ' + str(datetime.datetime.today())[:19] + '\n')
                f.close()
                exit()
        return BeautifulSoup(default_page.text, 'html.parser').find('input', {'id': '__VIEWSTATE'}).get('value')

    def get_all_page_data(self, view_tag, target_url):
        view_tag_list = [view_tag]

        pass

    def set_error_log(self, file):
        self.__error_log = file

    def get_error_log(self):
        return self.__error_log


print(str(datetime.datetime.today())[:19])
