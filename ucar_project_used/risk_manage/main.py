import pymysql
import risk_manage.add_title as add_title
import xlsxwriter

import ucar_project_used.risk_manage.sql_repository2 as sql2
from ignore import db_config as config


class RiskManage:
    def __init__(self):
        self.db = self.__connect_db()
        self.cursor = self.db.cursor()

    # 生成的excel文件名
    excel_name = './risk_manage2.xlsx'
    db = ''
    cursor = ''
    # 逾期用户uid
    uid_s = ''
    # 所有逾期用户
    over_due_users = ''
    # pengyuan 数据
    peng_yuan_data = ''
    # tongdun 相关数据
    tong_dun_main_data = ''
    tong_dun_risk_data = ''
    platform_data = ''
    fuzzy_data = ''
    fuzzy_content_data = ''
    frequency_data = ''
    follow_data = ''
    court_data = ''

    # 各个表的主要字段数量
    over_due_users_len = 10
    peng_yuan_len = 116

    def action(self):
        print('正在获取所有逾期用户......')
        self.get_all_over_due_users()
        print('ok..')
        print('正在获取pengyuan数据......')
        self.get_data_from_peng_yuan()
        print('ok..')
        print('正在获取所有tongdun数据......')
        self.get_all_data_from_tong_dun()
        print('ok..')
        print('开始将数据写入excel......')
        self.write_data_to_excel()
        print('done!!!!!!')

    def write_data_to_excel(self):
        try:
            # 创建excel
            workbook = xlsxwriter.Workbook(self.excel_name)
            worksheet = workbook.add_worksheet()
            # 插入表头
            add_title.add_title(worksheet, 0, 0)
            col = 1
            row = 0
            for user in self.over_due_users:
                # 将基础信息填入表格
                row2 = 0
                for i in user:
                    worksheet.write(col, row2, i)
                    row2 += 1

                # 将 pengyuan 数据写入表格
                row2 = self.process_and_write_pengyuan_data(self.peng_yuan_data, user[0], worksheet, col, row2)
                # 将tongdun数据写入表格
                row2 = self.process_and_write_tong_dun_data(self.tong_dun_risk_data, user[0], worksheet, col, row2)
                row2 = self.process_and_write_tong_dun_data(self.tong_dun_main_data, user[0], worksheet, col, row2, 1)
                row2 = self.process_and_write_tong_dun_data(self.platform_data, user[0], worksheet, col, row2)
                row2 = self.process_and_write_tong_dun_data(self.fuzzy_data, user[0], worksheet, col, row2)
                row2 = self.process_and_write_tong_dun_data(self.fuzzy_content_data, user[0], worksheet, col, row2)
                row2 = self.process_and_write_tong_dun_data(self.frequency_data, user[0], worksheet, col, row2)
                row2 = self.process_and_write_tong_dun_data(self.follow_data, user[0], worksheet, col, row2)
                self.process_and_write_tong_dun_data(self.court_data, user[0], worksheet, col, row2)
                row += 1
                col += 1
            # 固定表头
            worksheet.freeze_panes(1, 0)
        except Exception as e:
            print(e)
            exit()

    def process_and_write_pengyuan_data(self, data, uid, worksheet, col, row):
        for i in data:
            if i[1] == uid:
                for k in i[2:-1]:
                    worksheet.write(col, row, k)
                    row += 1
                break
        # 如果pengyuan没数据 默认为空
        if row < self.over_due_users_len + self.peng_yuan_len:
            for ii in range(self.peng_yuan_len):
                worksheet.write(col, row, '')
                row += 1
        return row

    @staticmethod
    def process_and_write_tong_dun_data(data, uid, worksheet, col, row, tongdun_main_or_not=0):
        concat_str = ''
        for i in data:
            if i[0] == uid:
                tmp = ''
                for j in i[1:]:
                    tmp += str(j) + '  '
                if len(concat_str) < 1:
                    concat_str = tmp
                else:
                    concat_str += ';' + tmp
                # st_tong_dun_main表中一个uid最多只有一条数据 所以当匹配到一条记录之后 就break
                if tongdun_main_or_not == 1:
                    break
        worksheet.write(col, row, concat_str)
        return row + 1

    def get_all_over_due_users(self):
        try:
            # 获取所有逾期用户信息
            self.cursor.execute(sql2.all_over_due_users())
            over_due_users = self.cursor.fetchall()
            self.over_due_users = over_due_users
            uid_s = ''
            for user in over_due_users:
                uid_s += ',' + str(user[0])
            self.uid_s = uid_s[1:]
            return self
        except Exception as e:
            print(e)
            exit()

    def get_data_from_peng_yuan(self):
        try:
            self.cursor.execute(sql2.credit_info(self.uid_s))
            peng_yuan_data = self.cursor.fetchall()
            self.peng_yuan_data = peng_yuan_data
            return self
        except Exception as e:
            print(e)
            exit()

    def get_all_data_from_tong_dun(self):
        try:
            # 获取并存储tongdun main risk表数据
            self.cursor.execute(sql2.tongdun_main(self.uid_s))
            self.tong_dun_main_data = self.cursor.fetchall()

            self.cursor.execute(sql2.tongdun_risk(self.uid_s))
            self.tong_dun_risk_data = self.cursor.fetchall()

            # 获取并存储tongdun子表数据
            self.cursor.execute(sql2.tongdun_vice_court(self.uid_s))
            self.court_data = self.cursor.fetchall()

            self.cursor.execute(sql2.tongdun_vice_follow(self.uid_s))
            self.follow_data = self.cursor.fetchall()

            self.cursor.execute(sql2.tongdun_vice_frequency(self.uid_s))
            self.frequency_data = self.cursor.fetchall()

            self.cursor.execute(sql2.tongdun_vice_fuzzy(self.uid_s))
            self.fuzzy_data = self.cursor.fetchall()

            self.cursor.execute(sql2.tongdun_vice_fuzzy_content(self.uid_s))
            self.fuzzy_content_data = self.cursor.fetchall()

            self.cursor.execute(sql2.tongdun_vice_platform(self.uid_s))
            self.platform_data = self.cursor.fetchall()
        except Exception as e:
            print(e)
            exit()

    @staticmethod
    def __connect_db():
        try:
            db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                                 passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
            return db
        except Exception as e:
            print(e)
            exit()

    def set_excel_name(self, excel_name):
        self.excel_name = excel_name


if __name__ == "__main__":
    class_ = RiskManage()
    class_.action()
