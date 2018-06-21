import os
import json
import pymysql
from ignore import db_config2 as db


def connect():
    try:
        database = pymysql.connect(host=db.host, port=db.port, user=db.user,
                                   passwd=db.pwd, db=db.db, charset=db.charset)
        return database
    except Exception as e2:
        print(e2)
        exit()


path = '/Users/zl/Desktop/6-20/vin'
files = os.listdir(path)
s = []
i = 1

db2 = connect()
cursor = db2.cursor()
for file in files:
    f = open(path + '/' + file, encoding='utf-8')

    iter_f = iter(f)
    str_ = ""
    for line in iter_f:
        str_ = str_ + line
    try:
        pass_res = json.loads(str_)['showapi_res_body']
        if pass_res['ret_code'] == 0:
            select_sql = "select uid from st_iou_papers_info where driving_license_id='%s'" % (pass_res['vin'])
            cursor.execute(select_sql)
            uid = cursor.fetchone()[0]
            sql = "insert into st_iou_papers_info_vin2 (uid,brand_name,model_name,sale_name,car_type,vin,engine_type,power,jet_type,fuel_Type,transmission_type,cylinder_number,cylinder_form,output_volume,made_year,air_bag,seat_num,vehicle_level,door_num,car_body,manufacturer,gears_num,car_weight,assembly_factory,made_month,car_line,stop_year,effluent_standard,fuel_num,guiding_price,year,remark,drive_style,created_at) VALUE (%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now())" % (uid,pass_res['brand_name'],pass_res['model_name'],pass_res['sale_name'],pass_res['car_type'],pass_res['vin'],pass_res['engine_type'],pass_res['power'],pass_res['jet_type'],pass_res['fuel_Type'],pass_res['transmission_type'],pass_res['cylinder_number'],pass_res['cylinder_form'],pass_res['output_volume'],pass_res['made_year'],pass_res['air_bag'],pass_res['seat_num'],pass_res['vehicle_level'],pass_res['door_num'],pass_res['car_body'],pass_res['manufacturer'],pass_res['gears_num'],pass_res['car_weight'],pass_res['assembly_factory'],pass_res['made_month'],pass_res['car_line'],pass_res['stop_year'],pass_res['effluent_standard'],pass_res['fuel_num'],pass_res['guiding_price'],pass_res['year'],pass_res['remark'],pass_res['drive_style'])
            print(uid)
            cursor.execute(sql)
            db2.commit()
    except Exception as e:
        print(e)
        pass
