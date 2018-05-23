import wx_sdk.wx_sdk as wx_sdk
import json
import base64
import requests
from bs4 import BeautifulSoup
import xlrd

# target_url = 'http://shixin.court.gov.cn/'
target_url = 'http://shixin.court.gov.cn/index_new_form.do'
post_search_url = 'http://shixin.court.gov.cn/findDisNew'
v_code_url = 'http://shixin.court.gov.cn/captchaNew.do'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'shixin.court.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


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


def action(name, id_card, n=5):
    i = 0
    while i < n:
        print('第' + str(i) + '次......')
        ss = requests.session()
        main_txt = ss.get(target_url, headers=headers).text
        captcha_id = BeautifulSoup(main_txt, 'html.parser').find('input', {'id': 'captchaId'}).get('value')
        v_code = ss.get(v_code_url + '?captchaId=' + captcha_id + '&random=0.4151782512538069').content
        with open('xx.jpeg', 'wb') as fs:
            fs.write(v_code)
            fs.close()
        v_code = input('please enter your v_code:')
        print(v_code)
        form_data = {
            'pName': name, 'pCardNum': id_card, 'pProvince': 0, 'pCode': v_code, 'captchaId': captcha_id
        }
        res = ss.post(post_search_url, data=form_data, headers=headers)
        if '验证码错误或验证码已过期' in res.text:
            i += 1
            continue
        # 如果验证码连续识别5次都失败
        if i == 5:
            print('验证码验证失败!!!!!!!!!')
            exit()
        return res.text


if __name__ == '__main__':

    workbook = xlrd.open_workbook('aaa2.xlsx')
    worksheet = workbook.sheet_by_index(0)
    width = worksheet.ncols
    height = worksheet.nrows
    stored_data = []
    try:
        for i in range(int((height - 1) / 6)):
            zx = action(worksheet.cell(i * 6 + 1, 1).value, worksheet.cell(i * 6 + 1, 2).value)
            if len(BeautifulSoup(zx, 'html.parser').findAll('tr')) > 1:
                stored_data.append([worksheet.cell(i * 6 + 1, 1).value, worksheet.cell(i * 6 + 1, 2).value])
                print('yes')
            else:
                print(str(i) + ' nonono!!!')
        print(stored_data)
    except Exception as e:
        print(e)
