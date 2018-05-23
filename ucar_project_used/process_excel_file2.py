import pymysql
import xlsxwriter
import time
from ignore import db_config as config


def connect_db():
    try:
        db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'], user=config.db_config['user'],
                             passwd=config.db_config['pwd'], db=config.db_config['db'], charset='utf8')
        return db
    except Exception as e:
        print(e)
        return False


# 导出所有代理商 未启用的用户，及相关信息
def task1():
    sql1 = "SELECT agent_realname,agent_id FROM st_agent_user WHERE agent_id=agent_parent AND agent_status=1 AND `abolish_time` IS NULL AND agent_id NOT IN (634,880,956,1711)"
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql1)
        agents_info = cursor.fetchall()
        workbook = xlsxwriter.Workbook('./store_excel/xxx2.xlsx')
        worksheet = workbook.add_worksheet()
        col = 0
        row = 0
        for name in agents_info:
            worksheet.write(row, col, name[0])
            aid = str(name[1])
            sql2 = "SELECT c.username,c.mobile,c.`create_time`,c.`send_money_time`,CASE c.package_id WHEN 95 THEN 10000 WHEN 96 THEN 20000 WHEN 145 THEN 15000 WHEN 152 THEN 10000 WHEN 151 THEN 20000 WHEN 150 THEN 15000 ELSE 0 END amount,b.token_num FROM st_agent_user a INNER JOIN `st_promote_token` b ON a.agent_id=b.aid INNER JOIN st_ucar_iou c ON SUBSTRING(c.ocode,3)=b.token_num LEFT JOIN `st_emergency_contact` d ON d.uid=c.uid WHERE (d.uid IS NULL OR d.number<5) AND a.agent_parent = '" + aid + "' AND c.`offline_process_status`=5 AND `send_money_time`>='2017-07-01 00:00:00'"
            cursor.execute(sql2)
            not_used_user_list = cursor.fetchall()
            row2 = 1
            print('writing ' + name[0] + '\'s consumer data to excel......')
            for consumer in not_used_user_list:
                worksheet.write(row2, col, consumer[0])
                worksheet.write(row2, col + 1, consumer[1])
                worksheet.write(row2, col + 2, str(consumer[2]))
                worksheet.write(row2, col + 3, str(consumer[3]))
                worksheet.write(row2, col + 4, consumer[4])
                worksheet.write(row2, col + 5, consumer[5])
                row2 += 1
            col += 7
            del not_used_user_list
        del agents_info
        workbook.close()
    except Exception as e:
        print(e)


# 查询代理商已通过 未放款的用户
def task2():
    agent_list = ["'王安'", "'尚晓文'", "'刘阳'", "'雷红明'", "'陈晓敏'"]
    # agent_list = ["'王安'"]
    # agent_list = ["'朱彦东'", "'张栖'", "'黄贵珍'", "'梁汉光'", "'白旭峰'", "'梁杰洪'"]
    agents = ','.join(agent_list)
    sql1 = "SELECT agent_id,agent_realname FROM st_agent_user WHERE agent_realname IN (" + agents + ") AND agent_id=agent_parent"
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute(sql1)
        agents_ = cursor.fetchall()
        workbook = xlsxwriter.Workbook('./store_excel/' + time.strftime("%Y%m%d") + '通过未放款.xlsx')
        worksheet = workbook.add_worksheet()
        col = 0
        row = 0
        for agent in agents_:
            worksheet.write(row, col, agent[1])
            aid = str(agent[0])
            sql2 = "SELECT c.username,c.mobile,CASE c.package_id WHEN 95 THEN 10000 WHEN 96 THEN 20000 WHEN 145 THEN 15000 WHEN 152 THEN 10000 WHEN 151 THEN 20000 WHEN 150 THEN 15000 ELSE 0 END amount,IF(c.`submit_time`,c.`submit_time`,c.create_time),'已通过(待放款)' STATUS,SUBSTRING(c.ocode,3) FROM st_agent_user a INNER JOIN `st_promote_token` b ON a.agent_id=b.aid INNER JOIN st_ucar_iou c ON SUBSTRING(c.ocode,3)=b.token_num LEFT JOIN `st_ucar_iou_log_transfer` d ON d.uid=c.uid WHERE d.uid IS NULL AND  c.`offline_process_status`=2 AND c.`credit_select_state`=3 AND a.agent_parent=" + aid + " AND c.create_time>'2017-07-01 00:00:00'"
            cursor.execute(sql2)
            customers = cursor.fetchall()
            row2 = 1
            print('正在将' + agent[1] + '的数据写入excel.....')
            for customer in customers:
                worksheet.write(row2, col, customer[0])
                worksheet.write(row2, col + 1, customer[1])
                worksheet.write(row2, col + 2, customer[2])
                worksheet.write(row2, col + 3, str(customer[3]))
                worksheet.write(row2, col + 4, customer[4])
                worksheet.write(row2, col + 5, customer[5])
                row2 += 1
            col += 7

    except Exception as e:
        print(e)


catalog_of_function_task = {
    'task1()': '导出所有代理商 未启用的用户，及相关信息',
    'task2()': '导出所有代理商 未启用的用户，及相关信息'
}

task2()
