import requests
from bs4 import BeautifulSoup

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

url = 'https://91mjw.com/all'
s = requests.Session()
r = s.get(url).text
soap = BeautifulSoup(r, 'html.parser')
info_list = soap.find_all('article', {'class': 'u-movie'})
for i in info_list:
    video_page = i.find('a')['href']
    # html5lib html.parser
    video_soap = BeautifulSoup(s.get(video_page).text, 'html5lib')
    # download resources
    down_list = video_soap.find('ul', {'id': 'download-list'})
    if down_list is not None:
        li_list = down_list.find_all('li')
        for li in li_list:
            name = li.find('span').text
            e2dk_href = li.select_one("a[href*=ed2k]")
            magnet_href = li.select_one("a[href*=magnet]")
            if e2dk_href is not None:
                e2dk = e2dk_href['href']
            if magnet_href is not None:
                magnet = magnet_href['href']
            # print(magnet)
            exit()
