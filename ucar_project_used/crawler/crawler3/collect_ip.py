import requests
from bs4 import BeautifulSoup

ip_domain1 = 'http://www.xicidaili.com'

common_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'httpbin.org',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Host': 'www.xicidaili.com',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

headers2 = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def collect_ip():
    res = requests.get('https://free-proxy-list.net/', headers=headers2, timeout=5)
    with open('ip/ip_list.html', 'w', encoding='utf-8') as fd:
        fd.write(res.text)
        fd.close()
    print('done!!!')


# collect_ip()
def get_ip_and_write_to_file():
    text = BeautifulSoup(open('ip/ip_list.html', 'r'), 'html.parser')
    table = text.find('table', {'id': 'proxylisttable'})
    tr = table.findAll('tr')
    for i in range(1, len(tr) - 1):
        if tr[i].findAll('td')[6].text == 'no':
            with open('ip/ip_list.txt', 'a') as fs:
                fs.write(str(tr[i].findAll('td')[0].text) + ':' + str(tr[i].findAll('td')[1].text) + '\n')

    print('done!!!!')


proxies = {
    'http': '101.201.115.184:8080',
}
# ip_test_url = 'http://httpbin.org/ip'
url1 = 'http://admintest.51ucar.cn/xx/aa/ip_address'
url2 = ''
ip_test_url = 'http://admintest.51ucar.cn/xx/aa/ip_address'
text1 = requests.get(ip_test_url, proxies=proxies, headers=common_headers).text
print(text1)
