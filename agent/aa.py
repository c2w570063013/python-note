import requests
import json
import pymysql
import db_config as config

# print(db.db_config['host'])
# exit()

session = requests.session()
mobile = '17724689539'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6,ms;q=0.5,mt;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}


def test():
    url_test = 'http://ucar_agent.test/test'
    res = session.get(url_test, headers=headers)
    print(res)


def connect_db():
    db_config = {
        'host': config.db_config['host'],
        'port': config.db_config['port'],
        'user': config.db_config['user'],
        'pwd': config.db_config['pwd'],
        'db': config.db_config['db'],
        'charset': config.db_config['charset']
    }
    try:
        db = pymysql.connect(host=db_config['host'], port=db_config['port'], user=db_config['user'],
                             passwd=db_config['pwd'], db=db_config['db'], charset='utf8')
        return db
    except Exception as e:
        print(e)
        exit()


def get_v_code():
    url = 'http://ucar_agent.test/login/code'
    params = {
        'mobile': mobile,
    }
    try:
        res = session.post(url, headers=headers, data=params)
        if res.status_code == 200:
            db = connect_db()
            cursor = db.cursor()
            sql = "SELECT content FROM push_sms WHERE `mobile`=%s ORDER BY created_at DESC LIMIT 1" % mobile
            cursor.execute(sql)
            record = cursor.fetchone()
            return int(json.loads(record[0])['code'])
        else:
            print('error')

    except Exception as e:
        print(e)


def simulate_login():
    v_code = get_v_code()
    if not v_code:
        print('get v_code failed!!!')
        exit()
    url = 'http://ucar_agent.test/login/'
    params = {
        'code': v_code,
        'login_name': mobile
    }
    try:
        res = session.put(url, headers=headers, data=params)
        print(res.text)
    except Exception as e:
        print(e)


def access_user():
    url = 'http://ucar_agent.test/user'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    # headers['Authorization'] = 'Bearer'+' eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjY5MTQ4N2UzZTVlMWU5Njk0MjdmMzQ0NDkxNTgwNzcwYmY0YjM5MGIyZjVhY2Q2NzgxMjQwMThhN2I1NmFhNDRhNWI3ZDhhMzQ2NzI1YjU0In0.eyJhdWQiOiIyIiwianRpIjoiNjkxNDg3ZTNlNWUxZTk2OTQyN2YzNDQ0OTE1ODA3NzBiZjRiMzkwYjJmNWFjZDY3ODEyNDAxOGE3YjU2YWE0NGE1YjdkOGEzNDY3MjViNTQiLCJpYXQiOjE1MjM2ODU5NjUsIm5iZiI6MTUyMzY4NTk2NSwiZXhwIjoxNTI0OTgxOTY1LCJzdWIiOiIxIiwic2NvcGVzIjpbImFnZW50Il19.vBMjM2s1Qjk4R9bvBss_ATcKrjJzswqG7LNPqXhJxwPumcpCJSDLL7m215EbF7ltCQgt5JEINCqyhIXuwDBSloUgVtceHdlQ-qZXjHejOjOBZroLU6s7sOCAjO47mcLWYP4GF1zzIb3GrETONkQLgD2xzGUm_W38rYSPRPBszFVHfz8pP8Bs9wxvzGTZ2HbtB_87CEDNnRhy5J-om2tN_1ppOKE0jnNXshqX2HfcZBKWjOdEAS_yoYGp8WCEcdjLXUJeWcHY8e_yXi0Ly9yBQ-nEIowwPO1C-zDQYT9PCEKsMgpb9i_QHsJj3iqkkVBOO_HbEFvGW0FHvlTeYHQeKIpDGru5nGO4FfjxmWZdJYSJg4WtOyyXu-ya7-_KyV3P6DmghyvM3RltlpYHPCh4fhy_d1AankADE2isPDXqfqFejerZJgPg36O0k2nCheqxMCInLDLgQv5S6BAf4o2REnmlQ1UZBdEop9xPz5l_OErfWoWHdc3VZ6lP0Px0IvYccyQq8Il5IcHCjU7w-o3x2MtMMJmqLURBzWWCNgeqcRY5n3G8Gi6O-azfnqTzW_llEcNZN6BwHSHhaDSjz6PjAGJj1WDkuR5Rgo6-4WmkdIUShJJaSdL_YU_5fqUcFQteS-h21JxPczKWeZRmuT-aDLJ2mJexd_1e6R2blSMSlWQ'
    headers[
        'Authorization'] = 'Bearer' + ' eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhlYjc1ODk0YzA2M2M1YmQ1Y2Q2Mzc3YjkyMzc5MWQzNDFlNjM0MGQyY2MwODYyYTZmYzI2YzIwZmFmMThiZGFmMTQyM2I1NmYxMDM5NTVlIn0.eyJhdWQiOiIyIiwianRpIjoiOGViNzU4OTRjMDYzYzViZDVjZDYzNzdiOTIzNzkxZDM0MWU2MzQwZDJjYzA4NjJhNmZjMjZjMjBmYWYxOGJkYWYxNDIzYjU2ZjEwMzk1NWUiLCJpYXQiOjE1MjQ1NTg1ODksIm5iZiI6MTUyNDU1ODU4OSwiZXhwIjoxNTI1ODU0NTg5LCJzdWIiOiIzIiwic2NvcGVzIjpbImFnZW50Il19.EaDAJRrZ_VfEvL_mlcA94uKfQgQ1mdIm6PCCH69GmrSzdgz6SkCfCRXOZu5HexRXxIfugBKoRcbfKeYykt28kARXhhFWUiLQFUi_kuQEPZOHya9FlGzjGPQi-iHsGU2UMcK-cX_wUmxa8yrrnSYkhV4Qs4uKKqMCwpT8g6-6dVUv-kY7YQhd8uIybkQ9LaX1c2poDHMf0sZ2BxeeCDgBmEsRHFaivdU_9T8l5XNKiob99nryzAnh8EEUV_yF2lA-Dfa-ye9oKAoq1ROM_t-dsHNzPcJL5oegzgGXXM2jdNx9OoDMpjXOj-vvl-zh0H36aGWyLIwIdcAsajhG68oErq9WeL6GFVltYuBCwbkvOccHKOqbFbop9CZVISNWhYrUjUoABDKk5N8aOsIlFDHooP6uo03dM4wWi3YYRGzjBA7Ez6opvCwRLsHeA78YgxbGJzoNlpsZWWELYQzjrxzccoO55YqY_rGI5Hc7U626TG9C0f7WUslZ56NDoQ8shLh9eV0V5lq_DnovgPKZ7oYCxN8G5txFgOEuMOA2v8xnp6sL7bPT4vqknSSMUwuAWquzc70YI3bT0mMDbF0gncJl0MNyfxLqb7fog6jQngjTRgmeQ9rvuEf22EBwgRciMMlaYmEF2LFuYqPphxhkmEW2PxhGzA-PJqKBiGiFwzM8c-M'
    x = requests.get(url, headers=headers)
    print(x.text)
    # print(headers)


simulate_login()
# access_user()
