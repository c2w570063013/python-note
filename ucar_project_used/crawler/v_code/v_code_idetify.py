import urllib.request as urllib2
import requests
import json


class IdentifyVCode:
    interface_url = 'https://way.jd.com/showapi/checkcode_math'
    app_key = '0ee0ddf3367f12894c190e021a71c3b0'

    def __init__(self, base64_img):
        self.base64_img = base64_img

    @staticmethod
    def file_get_contents(filename, use_include_path=0, context=None, offset=-1, maxlen=-1):
        if (filename.find('://') > 0):
            ret = urllib2.urlopen(filename).read()
            if (offset > 0):
                ret = ret[offset:]
            if (maxlen > 0):
                ret = ret[:maxlen]
            return ret
        else:
            fp = open(filename, 'rb')
            try:
                if (offset > 0):
                    fp.seek(offset)
                ret = fp.read(maxlen)
                return ret
            finally:
                fp.close()

    def wx_post_req(self, url, params, img=None, bodyStr=None):
        ret = self.file_get_contents(img) if img else bodyStr
        return requests.post(url, params=params, data=ret)

    def return_identify_res(self):
        base64_img = 'img_base64=' + str(self.base64_img, 'utf-8')
        res = self.wx_post_req(self.interface_url, {'appkey': self.app_key}, bodyStr=base64_img)
        res_dic = json.loads(res.text)
        if res_dic['msg'] == '查询成功':
            return res_dic['result']['showapi_res_body']['Result']
        return False


if __name__ == '__main__':
    # example
    import base64
    v_code_url = 'http://www.sinopecsales.com/websso/YanZhengMaServlet'
    base64_img_ = base64.b64encode(requests.get(v_code_url).content)
    identifyC = IdentifyVCode(base64_img_)
    res1 = identifyC.return_identify_res()
    print(res1)
