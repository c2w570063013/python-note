import xlsxwriter
import pymysql
import datetime
import pandas
import requests
import tensorflow
from ignore import db_config as config





def connect_db():
    try:
        db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                             passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
        return db
    except Exception as e:
        print(e)
        exit()


def out_put(time_start, time_end):
    try:
        db = connect_db()
        cursor = db.cursor()
        # date_1 = datetime.datetime.strptime(time_start, "%Y%m%d")
        workbook = xlsxwriter.Workbook('data.xlsx')
        worksheet = workbook.add_worksheet()
        # 写入横抬头 代理商
        agent_sql = "SELECT agent_realname FROM st_agent_user WHERE agent_id=agent_parent AND agent_status=1 AND `abolish_time` IS NULL AND agent_id NOT IN (634,956,1711,2526)"
        cursor.execute(agent_sql)
        agent_list = cursor.fetchall()
        col = 1
        row = 0
        # 将代理商名字存入列表
        agent_list_ = []
        for i in agent_list:
            agent_list_.append(i[0])
            worksheet.write(row, col, i[0])
            col += 1
        agent_dic = map_to_agent(agent_list_)
        worksheet.write(row, col, '代理商总和')
        worksheet.write(row, col + 1, '优卡白条-公司')
        delta = datetime.datetime.strptime(time_end, "%Y-%m-%d") - datetime.datetime.strptime(time_start, "%Y-%m-%d")
        date_arr = [time_start]

        n_row = 1
        n_col = 0
        for i in range(delta.days + 1):
            if i == 0:
                add_time = 0
            else:
                add_time = 1
            date_x = datetime.datetime.strptime(date_arr[i], "%Y-%m-%d") + datetime.timedelta(days=add_time)
            date_1 = str(date_x)[:10]
            # 写入纵抬头 时间
            worksheet.write(n_row, n_col, date_1)
            date_arr.append(date_1)
            sql1 = "SELECT (SELECT agent_realname FROM st_agent_user WHERE agent_id=a.agent_parent) agent_parent,count(c.id) num FROM st_agent_user a INNER JOIN `st_promote_token` b ON a.agent_id=b.aid INNER JOIN st_ucar_iou c ON SUBSTRING(c.ocode,3)=b.token_num WHERE a.agent_parent IN (SELECT agent_id FROM st_agent_user WHERE agent_id=agent_parent AND agent_status=1 AND `abolish_time` IS NULL) AND DATE_FORMAT(c.create_time, '%Y-%m-%d')='" + date_1 + "' GROUP BY a.agent_parent ORDER BY num DESC;"
            cursor.execute(sql1)
            data = cursor.fetchall()
            # 所有代理商收单总和
            agent_total_register = 0
            for ii in data:
                if ii[0] in agent_dic:
                    worksheet.write(n_row, agent_dic[ii[0]], ii[1])
                    agent_total_register += int(ii[1])
            # 写入代理商收单总和
            worksheet.write(n_row, len(agent_list_) + 1, agent_total_register)
            # 公司优卡白条收单sql
            sql2 = "SELECT count(id) FROM st_ucar_iou WHERE DATE_FORMAT(create_time, '%Y-%m-%d')='" + date_1 + "';"
            cursor.execute(sql2)
            data2 = cursor.fetchone()
            # 写入公司当日收单
            worksheet.write(n_row, len(agent_list_) + 2, data2[0])
            n_row += 1
            print(data)
            print('----------------------------------------')
    except Exception as e:
        print(e)


def map_to_agent(agent_list):
    dic = {}
    j = 1
    for i in agent_list:
        dic[i] = j
        j += 1

    return dic


# out_put('2018-01-01', '2018-03-22')
