from openpyxl import load_workbook
import requests
from bs4 import BeautifulSoup
import datetime
import re
import sys
import os
import json


def parse_excel(file_path):
    try:
        wb = load_workbook(filename=file_path)
        sheet = wb.active
        max_column = sheet.max_column
        max_row = sheet.max_row
        start_row = 7
        start_col = 2
        # first step, add email and domain to the sheet tittle
        sheet.cell(row=start_row - 1, column=max_column + 1).value = 'Email'
        sheet.cell(row=start_row - 1, column=max_column + 2).value = 'Domain'

        # start to iterate the excel and search for the info
        for i in range(start_row, max_row + 1):
            cell_value = sheet.cell(row=i, column=start_col).value.strip()
            process_val = re.sub('Co.{1,4}Ltd.', '', cell_value, flags=re.IGNORECASE)
            print('start scrap company:' + process_val)
            process_res = scrape(process_val.strip())
            if process_res is False:
                continue
            sheet.cell(row=i, column=max_column + 1).value = process_res['email']
            sheet.cell(row=i, column=max_column + 2).value = process_res['domain']
        # save the excel
        wb.save(file_path)
        print('--------------done--------------')

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('whoops, error happen! error:' + str(e), exc_type, fname, exc_tb.tb_lineno)


def scrape(keyword):
    try:
        url = 'https://exhibitors.electronica.de/onlinecatalog/2018/Search_result/'
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
        params = {
            "LNG": 2,
            "nv": 1000,
            "sb_n": "suche",
            "sb_m": 1100,
            "sb_c": 15,
            "pag_styp": 1,
            "sb1_t": "basic",
            "sb1_v": "text",
            "sb1_n": "suche",
            "sb1_searchRequests": "ex,pd",
            "sb1_defaultSearchRequests": "ex,pd",
            "sb2": "ex,pd",
            "sb2_n": "bereiche",
            "sb2_t": "ignoreCondition",
            "sb1": keyword
        }
        res = requests.post(url, data=params, headers=headers, timeout=15)
        if res.status_code != 200:
            raise Exception('network error!', 'status_code' + str(res.status_code))
        soup = BeautifulSoup(res.text, 'html.parser')
        # find the target element
        target = soup.find_all('a', {"class": 'exd_navfont'})
        if len(target) == 0:
            print('keyword:' + keyword + ' empty')
            record_to_log('keyword:' + keyword + '; result:empty', 'empty.log')
            return False

        res_list = {}
        for a in target:
            a_val = a.text.strip()
            # determine if value is email
            if '@' in a_val:
                res_list['email'] = a_val
                continue
            res_list['domain'] = a_val + ' '
        # if no specific key in return value, set default '' to it
        if 'email' not in res_list:
            res_list['email'] = ''
        if 'domain' not in res_list:
            res_list['domain'] = ''
        record_to_log('keyword:' + keyword + '; result:' + json.dumps(res_list), 'success.log')
        return res_list
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)
        record_to_log('keyword:' + keyword + '; error:' + str(e), 'error.log')
        return False


def record_to_log(content, file='log.txt'):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = open(file, 'a')
    f.write('[' + time + '] ' + content + "\n")


file_ = '(Automotive).xlsx'
parse_excel(file_)
