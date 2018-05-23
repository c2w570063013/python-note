import requests
from bs4 import BeautifulSoup


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


if __name__ == '__main__':
    ip_pool = IpPool()
    ip = ip_pool.get_ip()
    print(ip)
