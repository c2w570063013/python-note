import pymysql
from ignore import db_config as config


def connect_db():
    try:
        db = pymysql.connect(host=config.db_config['host'], port=config.db_config['port'],
                             user=config.db_config['user'],
                             passwd=config.db_config['pwd'], db=config.db_config['db'],
                             charset=config.db_config['charset'])
        return db
    except Exception as e:
        print(e)
        exit()


def task1(*argv):
    """
    :arg agent_name
    :param argv:
    :return:
    """
    # get_aid_sql = ""
    # sql = "SELECT c.create_time,d.`set_auth_status_time`,c.mobile,CASE c.package_id WHEN 95 THEN 10000 WHEN 96 THEN 20000 WHEN 145 THEN 15000 WHEN 152 THEN 10000 WHEN 151 THEN 20000 WHEN 150 THEN 15000 ELSE 0 END package,e.identification FROM st_agent_user a INNER JOIN `st_promote_token` b ON a.agent_id=b.aid INNER JOIN st_ucar_iou c ON SUBSTRING(c.ocode,3)=b.token_num INNER JOIN `st_aiqianbang_record_status` d ON d.uid=c.uid LEFT JOIN st_ucar_iou_file e ON e.uid=c.uid WHERE a.`agent_parent`= 2644 AND c.`offline_process_status`=2 AND c.`credit_select_state`=3 AND c.`is_icbind`=2 AND d.`set_auth_status`=1"
    # pass
    str1 = ''
    for arg in argv:
        # print("another arg through *argv :", arg)
        str1 += arg + ','
    print(str1)


task1('dfsdf', 'dsfdsfs', 'ksdfkds')
