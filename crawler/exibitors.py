from openpyxl import Workbook
from openpyxl import load_workbook
import requests
from bs4 import BeautifulSoup


def parse_excel():
    wb = load_workbook(filename='(Automotive).xlsx')
    sheet = wb.active
    # get cell value
    xx = sheet.cell(row=3, column=2).value
    max_column = sheet.max_column
    max_row = sheet.max_row
    # print(xx, max_column, max_row)

    company_1 = sheet.cell(row=7, column=2).value
    print(company_1.strip())


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
        res = requests.post(url, data=params, headers=headers)
        if res.status_code != 200:
            raise Exception('network error!', 'status_code' + str(res.status_code))
        soup = BeautifulSoup(res.text, 'html.parser')
        target = soup.find_all('a', {"class": 'exd_navfont'})
        if len(target) == 0:
            return False
        if len(target) == 1:
            return [target[0].text.strip(), '']
        if len(target) == 2:
            return [target[0].text.strip(), target[1].text.strip()]
    except Exception as e:
        print(e)
        return False


def record_to_log():

    pass


real_res = scrape('Ohnuki Manufacturing Industry')
print(real_res)
