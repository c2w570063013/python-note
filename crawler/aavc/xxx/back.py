import datetime
import base64

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


class IpPool:
    __headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    # this url only contains http ip chunks
    __ip_content_url = 'http://www.xicidaili.com/wt/'

    __check_ip_is_alive_url = 'http://admintest.51ucar.cn/xx/aa/ip_address'

    def get_ip(self):
        page = 1
        while page <= 10:
            print('current page is ' + str(page) + ' ......')
            text = requests.get(self.__ip_content_url + str(page), headers=self.__headers).text
            res = self.parse_html_and_return_ip(text)
            if res is not False:
                return res
            page += 1

    def parse_html_and_return_ip(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        trs = soup.find('table', {'id': 'ip_list'}).findAll('tr')
        # the first tr is title info so subtract 1
        length = len(trs) - 1
        int_len = 1
        for tr in trs[1:]:
            print('current tr is' + str(int_len))
            current_tds = tr.findAll('td')
            # only collect anonymous ips
            if current_tds[4].text == '高匿':
                # check if ip is available
                if self.check_ip_is_enable(current_tds[1].text, current_tds[2].text) is True:
                    return current_tds[1].text + ':' + current_tds[2].text
            if int_len == length:
                return False
            int_len += 1

    def check_ip_is_enable(self, ip, port):
        proxies = {
            'http': str(ip) + ':' + str(port)
        }
        try:
            res = requests.get(self.__check_ip_is_alive_url, headers=self.__headers, proxies=proxies, timeout=3)
            if res.status_code == 200:
                return True
        except:
            return False


class RedisQueue(object):
    """Simple Queue with Redis Backend"""


def qsize(self):
    """Return the approximate size of the queue."""
    return self.__db.llen(self.key)


def empty(self):
    """Return True if the queue is empty, False otherwise."""
    return self.qsize() == 0


def put(self, item):
    """Put item into the queue."""
    self.__db.rpush(self.key, item)


def get(self, block=True, timeout=None):
    """Remove and return an item from the queue.

    If optional args block is true and timeout is None (the default), block
    if necessary until an item is available."""
    if block:
        item = self.__db.blpop(self.key, timeout=timeout)
    else:
        item = self.__db.lpop(self.key)

    if item:
        item = item[1]
    return item


def get_nowait(self):
    """Equivalent to get(False)."""
    return self.get(False)
