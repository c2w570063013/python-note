import requests
from bs4 import BeautifulSoup
import pymysql
from ignore import db_config as config


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

    def get_all_content(self, n=5):
        for i in range(n):
            print('getting and parsing ' + str(i + 1) + ' page......')
            target_url = self.__ip_content_url + str(i + 1)
            self.get_single_content(target_url)

    def get_single_content(self, url):
        text = requests.get(url, headers=self.__headers).text
        soup = BeautifulSoup(text, 'html.parser')
        trs = soup.find('table', {'id': 'ip_list'}).findAll('tr')
        for tr in trs[1:]:
            current_tds = tr.findAll('td')
            if self.check_ip_is_alive_from_content(current_tds[1].text, current_tds[2].text) is True:
                location = '未知' if current_tds[3].find('a') is None else current_tds[3].find('a').text
                print('saving ' + current_tds[1].text + ' to db......')
                self.__insert_into_db(current_tds[1].text, current_tds[2].text, current_tds[4].text,
                                      location, current_tds[9].text)

    def check_ip_is_alive_from_content(self, ip, port):
        proxies = {
            'http': str(ip) + ':' + str(port)
        }
        try:
            res = requests.get(self.__check_ip_is_alive_url, headers=self.__headers, proxies=proxies, timeout=5)
            if res.status_code == 200:
                return True
        except:
            return False

    def __insert_into_db(self, ip, port, attr, location, duration_time):
        db = self.__connect_db()
        cursor = db.cursor()
        sql = "INSERT INTO ip_pool (`ip`,`port`,`attribute`,`location`,`duration_time`,`create_time`) VALUES ('" + ip + "'," + port + ",'" + attr + "','" + location + "','" + duration_time + "',now())"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('insert error, sql:' + sql)
            db.rollback()

    @staticmethod
    def __connect_db():
        db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                             passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
        return db

    def check_ip_is_still_alive_from_db(self):
        pass


if __name__ == '__main__':
    ip_pool = IpPool()
    ip_pool.get_all_content()
cookies = 'x'

res = requests.get('http://admintest.51ucar.cn/xx/aa/ip_address', proxies={'http': '162.243.187.230:81'},
                   cookies=cookies).text
print(res)
