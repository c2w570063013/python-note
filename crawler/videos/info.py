import db_config
import pymysql

main_url = 'https://91mjw.com'
url = 'https://91mjw.com/all'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "91mjw.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15",
    "Accept-Language": "en-us"
}


def connect_db():
    try:
        db = pymysql.connect(host=db_config.host, port=db_config.port, user=db_config.user,
                             passwd=db_config.pwd, db=db_config.db, charset='utf8')
        return db
    except Exception as e:
        print(e)
        exit()


# images saved path
cover_path = '/Users/wayne/code/bit-trade/public/images/covers/'
plot_img_path = '/Users/wayne/code/bit-trade/public/images/plot_img/'
