import requests
import base64
import crawler.wx_sdk.wx_sdk as wx_sdk
import json
from bs4 import BeautifulSoup
import re
import datetime
import inspect
import pymysql
from ignore import db_config as config


# 识别验证码
def identify_v_code(base_64_img):
    url = 'https://way.jd.com/showapi/checkcode_ys'
    body_str = 'img_base64=' + str(base_64_img, 'utf-8')
    params = {
        'typeId': '34',
        'convert_to_jpg': '0',
        'appkey': '1c4d515b1908c1700015b5d83855ea66'
    }
    response = wx_sdk.wx_post_req(url, params, bodyStr=body_str)
    return json.loads(response.text)['result']['showapi_res_body']['Result']


# 模拟登陆
def simulate_login(login_url, v_code_url, consumed_page_url, time_start, time_end, consumed_or_top_up=1):
    print('get cookie from url......')
    cookie = requests.get(login_url).cookies
    login_post_data = {
        'ctl00$ContentPlaceHolder1$txtID': '50042742',
        'ctl00$ContentPlaceHolder1$txtPWD': 'ucar99882016',
        'ctl00$ContentPlaceHolder1$txtCheck': '',
        '__VIEWSTATE': '/wEPDwUKMTQxMDQ4NDAyMmRkobdBOsFxX2WDVDhsoxI9GxIOTLw=',
        'ctl00$ContentPlaceHolder1$btnLogin': '50042742'
    }

    # 判断是否登陆成功 最多尝试登陆5次
    for i in range(5):
        print('get v_code and convert to base64 img')
        base_64_img = base64.b64encode(requests.get(v_code_url, cookies=cookie).content)
        print('identifying v_code......')
        code_res = identify_v_code(base_64_img)
        login_post_data['ctl00$ContentPlaceHolder1$txtCheck'] = code_res
        print('logging in......')
        login_res = requests.post(login_url, data=login_post_data, cookies=cookie).text
        if 'WebAccountDetail.aspx' in login_res.encode('ascii', 'ignore').decode('utf-8'):
            print('login successfully!!')
            break
        if i == 4:
            with open('error.log', 'a', encoding='utf-8') as f:
                f.write('多次登陆验证失败\n')
                f.close()
                exit()

    # 获取登陆成功后默认进入的页面
    default_content = requests.get(consumed_page_url, cookies=cookie)
    # 默认页面识别符
    default_view_state = BeautifulSoup(default_content.text, 'html.parser').find('input', {'id': '__VIEWSTATE'}).get(
        'value')
    filter_post_data = {
        'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$updatepannel1|ctl00$ContentPlaceHolder1$btnSearch',
        '__VIEWSTATE': default_view_state,
        'ctl00$ContentPlaceHolder1$ddlDateType': 1,
        'ctl00$ContentPlaceHolder1$ddlShift': 0,
        'ctl00$ContentPlaceHolder1$btnSearch': '查询',
        'ctl00$ContentPlaceHolder1$txtDate1': time_start,
        'ctl00$ContentPlaceHolder1$txtDate2': time_end
    }
    print('obtain the main page data.....')
    # 筛选页面首页
    filter_data_page = requests.post(consumed_page_url, data=filter_post_data, cookies=cookie)
    if filter_data_page.status_code == 200:
        soup2 = BeautifulSoup(filter_data_page.text, 'html.parser')
        default_view_state2 = soup2.find('input', {'id': '__VIEWSTATE'}).get('value')
        page_info = soup2.select('span#ctl00_ContentPlaceHolder1_lblinfo')[0].text
        page_info_num = re.findall('\d+', page_info)
        # 如果条数为0 则退出
        if int(page_info_num[0]) == 0:
            exit()
        # 总页数
        total_pages = int(page_info_num[1])
        # 将第一页数据解析并插入至数据库中
        print('parse 1 page dom and save data to db......')
        parse_dom_and_save_data_to_db(filter_data_page.text, consumed_or_top_up)
        # 将剩余的页数循环遍历
        loop_all_page_and_get_data(default_view_state2, consumed_page_url, total_pages, cookie, time_start, time_end,
                                   consumed_or_top_up)
    else:
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write('获取数据失败\n')
            f.close()
            exit()


# 循环页面 并将数据写入文件
def loop_all_page_and_get_data(default_state, target_url, total_pages, cookie, time_start, time_end,
                               consumed_or_top_up=1):
    filter_post_data2 = {
        'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$updatepannel2|ctl00$ContentPlaceHolder1$btnnext',
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btnnext',
        '__VIEWSTATE': '',
        'ctl00$ContentPlaceHolder1$txtDate1': time_start,
        'ctl00$ContentPlaceHolder1$txtDate2': time_end
    }
    view_state_list = [default_state]
    for i in range(total_pages - 1):
        print('parse ' + str(i + 2) + ' page dom and save data to db......')
        filter_post_data2['__VIEWSTATE'] = view_state_list[0]
        del view_state_list
        view_state_list = []
        res = requests.post(target_url, filter_post_data2, cookies=cookie)
        if res.status_code == 200:
            parse_dom_and_save_data_to_db(res.text, consumed_or_top_up)
        else:
            with open('error.log', 'a') as fd:
                fd.write(
                    '获取数据失败' + inspect.currentframe().f_code.co_filename + '第' +
                    inspect.currentframe().f_lineno + '行' +
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                fd.close()

        view_state = BeautifulSoup(res.text, 'html.parser').find('input', {'id': '__VIEWSTATE'}).get('value')
        view_state_list.append(view_state)

    del view_state_list
    del filter_post_data2


def connect_db():
    db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                         passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
    return db


def parse_dom_and_save_data_to_db(html_content, consumed_or_to_up=1):
    html = BeautifulSoup(html_content, 'html.parser')
    table = html.find('table', {'id': 'ctl00_ContentPlaceHolder1_tbNews'})
    tr = table.findAll('tr')
    db = connect_db()
    cursor = db.cursor()

    tmp_val_list = []
    for i in tr[1:]:
        td = i.findAll('td')
        for j in td[1:]:
            span_val = j.find('span').text
            tmp_val_list.append(span_val)

        date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if consumed_or_to_up == 1:
            oil = re.findall('\d+', tmp_val_list[3])
            oil_type = 'NULL'
            if len(oil) > 0:
                oil_type = oil[0]
            insert_sql = "INSERT INTO la_bp_consumed_detail (account,oil_card_num,petrol_station,consumed_item,petrol_price,discount_price,consumed_price,after_discount_price,consumed_amount,car_id_num,consumed_time,oil_type,created_at) " \
                         "VALUES (" + tmp_val_list[0] + "," + tmp_val_list[1] + ",'" + tmp_val_list[2] + "','" + \
                         tmp_val_list[3] + "'," + tmp_val_list[4] + "," + tmp_val_list[5] + "," + tmp_val_list[
                             6] + "," + tmp_val_list[7] + "," + tmp_val_list[8] + ",'" + tmp_val_list[9] + "','" + \
                         tmp_val_list[10] + "'," + oil_type + ",'" + date_now + "')"

        try:
            cursor.execute(insert_sql)
            db.commit()
        except:
            with open('error.log', 'a', encoding='utf-8') as f:
                f.write('插入错误 ' + insert_sql + '  ' + date_now)
            db.rollback()
        del tmp_val_list
        tmp_val_list = []
    db.close()


def action():
    login_url = 'http://card.bppc.com.cn/weblogin.aspx'
    v_code = 'http://card.bppc.com.cn/IdentifyCode.aspx'
    consumed_target_url = 'http://card.bppc.com.cn/WebConsumeDetail.aspx'
    time_start = '2017-12-04'
    time_end = '2017-12-04'
    simulate_login(login_url, v_code, consumed_target_url, time_start, time_end)


action()
