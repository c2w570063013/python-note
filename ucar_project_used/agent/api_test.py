import requests
import json


def test_insert():
    url = "http://ucar_agent.test/enjoy_api/apply_white_bar"

    info_data = {
        'code': 2,
        'data_info': [
            {"uid": 113, "token_code": 50018, "username": 'wayne', "mobile": 17777777777,
             "id_card": '452555565555555', "created_at": "2018-01-01 00:00:00"},
            {"uid": 114, "token_code": 50019, "username": 'wayne', "mobile": 17777777772,
             "id_card": '452555565555555x', "created_at": "2018-02-01 00:00:00"},
        ]
    }
    data = {
        'encrypt': '49e4e29829d0b786798c8c1f52fd9d0f',
        'data': json.dumps(info_data)
    }

    res = requests.post(url, data=data)
    print(res.text)


def test_update_user_info():
    url = "http://ucar_agent.test/enjoy_api/update_apply_info"
    info_data = {
        'code': 2,
        'data_info': [
            {'uid': 1, 'mobile': 15555555551, 'id_card': "555555555555555551", 'status': 2, 'package': 'none',
             "updated_at": '2018-04-10 00:00:00'},
            {'uid': 13, 'mobile': 15555555552, 'id_card': "555555555555555552", 'status': 5, 'package': '1',
             "updated_at": '2018-04-12 00:00:00'},
            {'uid': 14, 'mobile': 15555555553, 'id_card': "555555555555555553", 'status': 5, 'package': '2',
             "updated_at": '2018-04-12 00:00:00'}
        ]
    }
    data = {
        'encrypt': '49e4e29829d0b786798c8c1f52fd9d0f',
        'data': json.dumps(info_data)
    }
    res = requests.post(url, data=data)
    print(res.text)


test_update_user_info()
