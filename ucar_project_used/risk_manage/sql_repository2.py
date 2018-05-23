def all_over_due_users():
    # 10-1
    return "SELECT b.uid,b.username,CASE a.user_sex WHEN 1 THEN '男' WHEN 2 THEN '女' ELSE '未设置' END user_sex,DATE_FORMAT(now(), '%Y')-SUBSTRING(b.idcard,7,4) age,CASE b.marital_status WHEN 1 THEN '已婚' WHEN 0 THEN '未婚' ELSE '未知' END is_marry,concat(ifnull(b.seat_area,''),b.contact_address) user_address,b.mobile,DATEDIFF(now(), payment_time) over_due_days,12-cycle cycle,CASE package_id WHEN 95 THEN 10000 WHEN 96 THEN 20000 WHEN 145 THEN 15000 WHEN 152 THEN 10000 WHEN 151 THEN 20000 WHEN 150 THEN 15000 ELSE '其他' END package FROM `st_member` a INNER JOIN st_ucar_iou b ON a.id=b.uid WHERE b.`offline_process_status`>=4 AND b.`enable_status`=1 AND b.`finish`<>1 AND b.cycle<>12 AND DATEDIFF(now(), b.payment_time)>3"


def credit_info(uid_s):
    # 119-3
    return "SELECT * FROM `st_credit_info` WHERE uid IN (%s)" % uid_s


def tongdun_main(uid_s):
    # 3-1
    return "SELECT uid,final_decision,final_score FROM st_tongdun_main WHERE uid IN (%s)" % uid_s


def tongdun_risk(uid_s):
    # 5-1
    return "SELECT uid,item_name,risk_level,`group`,is_vice FROM st_tongdun_risk WHERE uid in (%s)" % uid_s


def tongdun_vice_court(uid_s):
    # 14-1
    return "SELECT uid,fraud_type,`name`,age,gender,province,filing_time,court_name,execution_department,duty,situation,discredit_detail,execution_base,case_number FROM st_tongdun_vice_court WHERE uid in (%s)" % uid_s


def tongdun_vice_follow(uid_s):
    # 5-1
    return "SELECT uid,description,fraud_type,hit_type_displayname,`type` FROM st_tongdun_vice_follow WHERE uid IN (%s)" % uid_s


def tongdun_vice_frequency(uid_s):
    # 3-1
    return "SELECT uid,detail,`data` FROM st_tongdun_vice_frequency WHERE uid IN (%s)" % uid_s


def tongdun_vice_fuzzy(uid_s):
    # 2-1
    return "SELECT uid,description FROM st_tongdun_vice_fuzzy WHERE uid IN (%s)" % uid_s


def tongdun_vice_fuzzy_content(uid_s):
    # 3-1
    return "SELECT uid,fraud_type,fuzzy_name FROM st_tongdun_vice_fuzzy_content WHERE uid IN (%s)" % uid_s


def tongdun_vice_platform(uid_s):
    # 3-1
    return "SELECT uid,dimension,`data` FROM st_tongdun_vice_platform WHERE uid IN (%s)" % uid_s
