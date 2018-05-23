import requests
import hashlib

v_code_url = 'http://www.saclub.com.cn/imgmerge?ranLen=4&text=%C8%C8%B5%E3%BE%DB%BD%B917989&imageFile=/new/img/f_yzm.jpg&x=24&y=24&fontColor=000000&fontStyle=bold&fontName=%CB%CE%CC%E5&fontSize=24'
login_post_url = 'http://www.saclub.com.cn/login.do'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}
main_index = 'http://www.saclub.com.cn/index.jsp'
login_main_info = {
    'username': 'ucar_123',
    'pwd': 'cai123456'
}


def simulate_login():
    v_code_res = requests.get(v_code_url, headers=headers)
    v_code = v_code_res.content
    cookie = v_code_res.cookies
    with open('bb.jpeg', 'wb') as fd:
        fd.write(v_code)
        fd.close()
    v_code2 = input('please enter your v_code:')
    login_form = {
        'mainGate': 'mysazone',
        'isFrom': 'index',
        'loginType': 'cardid',
        'userName': login_main_info['username'],
        'userPwd': hashlib.sha1(login_main_info['pwd'].encode('utf-8')).hexdigest(),
        'mask': v_code2
    }
    login_res = requests.post(login_post_url, data=login_form, headers=headers, cookies=cookie)

    # 判断是否登陆成功
    if "window.location.href='/logout.do'" not in login_res.text:
        raise Exception('login failed')

    print('login successfully!!!')


simulate_login()
