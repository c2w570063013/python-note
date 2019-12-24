import requests
from bs4 import BeautifulSoup
import random


# generate random string
def random_str(len_=8):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for ii in range(len_):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "exhibitors.electronica.de",
    "Origin": "https://exhibitors.electronica.de",
    "Referer": "https://exhibitors.electronica.de/onlinecatalog/2018/Search_result/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

s = requests.Session()
s.proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
url = 'https://www.jav321.com/star/1031775/2'
r = s.get(url).text
soap = BeautifulSoup(r, 'html.parser')
info_list = soap.find_all('div', {'class': 'thumbnail'})
print('downloading......')
ii = 1
for i in info_list:
    video_page = i.find('a')['href']
    video_soap = BeautifulSoup(s.get('https://www.jav321.com' + video_page).text, 'html.parser')
    source = video_soap.find('source')
    if source is not None:
        r = requests.get(source['src'], allow_redirects=True)
        open(random_str() + '.mp4', 'wb').write(r.content)
    print(ii)
    ii += 1

print('finished!!!!!!!')

