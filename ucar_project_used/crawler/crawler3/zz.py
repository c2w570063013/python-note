import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.xicidaili.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}


def collect_ip():
    target_ip_url = 'http://www.xicidaili.com/nn'
    res = requests.get(target_ip_url, headers=headers)
    with open('ip/ip1.txt', 'w', encoding='utf-8') as fd:
        fd.write(res.text)
        fd.close()
    print('done')


def parse_html_and_get_ip_list():
    file = open('ip/ip1.html', 'r', encoding='utf-8').read()
    soup = BeautifulSoup(file, 'html.parser')
    table = soup.find('table', {'id': 'ip_list'})
    tr = table.findAll('tr')
    for i in tr:
        for j in i.findAll('td'):
            print(j)
            # print(j[5])
            # if j[5] == 'HTTP':
                # with open('ip_list2.txt', 'a') as fd:
                #     fd.write(j[1] + ':' + j[2] + '\n')
                # print(j[1])
        # print(i)


# parse_html_and_get_ip_list()
xx = ['11']
xx.pop(0)
print(xx)
xx.append('22')
print(xx)