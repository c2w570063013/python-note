import urllib.request as urllib2
import requests
import json


class IdentifyCode:
    __identify_v_code_key = '1c4d515b1908c1700015b5d83855ea66'

    __type_id = 34

    __convert_to_jpg = 0

    __identify_url_interface = 'https://way.jd.com/showapi/checkcode_ys'

    @staticmethod
    def file_get_contents(filename, use_include_path=0, context=None, offset=-1, maxlen=-1):
        if filename.find('://') > 0:
            ret = urllib2.urlopen(filename).read()
            if offset > 0:
                ret = ret[offset:]
            if maxlen > 0:
                ret = ret[:maxlen]
            return ret
        else:
            fp = open(filename, 'rb')
            try:
                if offset > 0:
                    fp.seek(offset)
                ret = fp.read(maxlen)
                return ret
            finally:
                fp.close()

    def __wx_post_req(self, url, params, img=None, body_str=None):
        ret = self.file_get_contents(img) if img else body_str
        return requests.post(url, params=params, data=ret)

    '''识别验证码'''

    def identify_v_code(self, base_64_img, times=5):
        for i in range(times):
            body_str = 'img_base64=' + str(base_64_img, 'utf-8')
            params = {
                'typeId': self.__type_id,
                'convert_to_jpg': self.__convert_to_jpg,
                'appkey': self.__identify_v_code_key
            }
            response = self.__wx_post_req(self.__identify_url_interface, params, body_str=body_str)
            json_res = json.loads(response.text)
            if json_res['result']['showapi_res_body']['ret_code'] == 0:
                return json_res['result']['showapi_res_body']['Result']

            if i == 4:
                return False
