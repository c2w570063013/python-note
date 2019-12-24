# import urllib.request
# url_link = 'http://awspv3001.r18.com/litevideo/freepv/s/sni/snis00963/snis00963_dmb_w.mp4'
# urllib.request.urlretrieve(url_link, 'video_name.mp4')

import requests

# url = 'http://google.com/favicon.ico'
url = 'http://awspv3001.r18.com/litevideo/freepv/s/sni/snis00963/snis00963_dmb_w.mp4'
r = requests.get(url, allow_redirects=True)
open('xxx.mp4', 'wb').write(r.content)
