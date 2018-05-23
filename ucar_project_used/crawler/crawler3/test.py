import requests
import base64

# xx = requests.get('http://www.sinopecsales.com/websso/YanZhengMaServlet')
# img = base64.b64encode(xx.content)
# with open('img.txt', 'wb') as fd:
#     fd.write(img)
#     fd.close()
#
# with open('test.jpeg', 'wb') as fc:
#     fc.write(xx.content)
#     fc.close()

# proxies = {
#   'http': 'http://10.10.1.10:3128',
#   'https': 'http://10.10.1.10:1080',
# }

# proxies = {
#     'http': '40.83.113.27',
#     'https': '40.83.113.27'
# }

proxies = {
    'http': '47.89.41.164:80'
    # 'http': '112.114.99.22:8118',
    # 'https': '40.83.113.27',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Host': 'www.baidu.com',
    'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=requests%20proxy%20http%20%E7%AB%AF%E5%8F%A3&oq=requests%2520proxy%2520%25E7%25AB%25AF%25E5%258F%25A3&rsv_pq=d643240600062842&rsv_t=68b7%2BN1j4RAD9AX22cZTIluiLnaaY%2BlCwDli0hs2%2FYgufjegJWKtQ8ogM14&rqlang=cn&rsv_enter=1&inputT=1922&rsv_sug3=29&rsv_sug2=0&rsv_sug4=2338',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

headers2 = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Cache-Control': 'max-age=0',
    # 'Host': 'httpbin.org',
    'Proxy-Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

user_agent = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12 Version/12.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
]

# xx = requests.get('http://just_for_test.app/A_test/crawler/test2.php', proxies=proxies, headers=headers2)
try:
    xx = requests.get('http://httpbin.org/ip', headers=headers2, proxies=proxies)
    print(xx.text)
except Exception as e:
    print('yes')
# xx = requests.get('http://admintest.51ucar.cn/zzzz/xxxx/get_id', proxies=proxies)
# print(xx.text)
