import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "exhibitors.electronica.de",
    "Origin": "https://exhibitors.electronica.de",
    "Referer": "https://exhibitors.electronica.de/onlinecatalog/2018/Search_result/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
main_url = 'https://91mjw.com'
url = 'https://91mjw.com/all'
# turn pages
while True:
    print('scraping ' + url)
    s = requests.Session()
    r = s.get(url).text
    soap = BeautifulSoup(r, 'html5lib')
    info_list = soap.find_all('article', {'class': 'u-movie'})
    # traverse current page for getting videos links
    for i in info_list:
        video_page = i.find('a')['href']
        # html5lib html.parser
        video_soap = BeautifulSoup(s.get(video_page).text, 'html5lib')
        video_info = video_soap.find('div', {'class': 'video_info'})
        director_el = video_info.find('strong', text='导演:')
        director = ''
        if director_el is not None:
            director = director_el.next_sibling
        scriptwriter_el = video_info.find('strong', text='编剧:')
        scriptwriter = ''
        if scriptwriter_el is not None:
            scriptwriter = scriptwriter_el.next_sibling
        cast_el = video_info.find('strong', text='主演:')
        cast = ''
        if cast_el is not None:
            cast = cast_el.next_sibling
        area_el = video_info.find('strong', text='国家/地区:')
        area = ''
        if area is not None:
            area = area_el.next_sibling
        language_el = video_info.find('strong', text='语言:')
        language = ''
        if language_el is not None:
            language = language_el.next_sibling
        debut_date_el = video_info.find('strong', text='首播:')
        debut_date = ''
        if debut_date_el is not None:
            debut = debut_date_el.next_sibling
            l_bracket = debut.find('(')
            r_bracket = debut.find(')')
            debut_date = debut
            debut_area = ''
            if l_bracket != -1:
                debut_date = debut[:l_bracket]
                debut_area = debut[l_bracket + 1:r_bracket]
        season_el = video_info.find('strong', text='季数:')
        season = 1
        if season_el is not None:
            season = season_el.next_sibling
        episode_num_el = video_info.find('strong', text='集数:')
        episode_num = 0
        if episode_num_el is not None:
            episode_num = int(episode_num_el.next_sibling)
        episode_time_el = video_info.find('strong', text='单集时长:')
        episode_time = ''
        if episode_time_el is not None:
            episode_time = episode_time_el.next_sibling
        alias_el = video_info.find('strong', text='又名:')
        alias = ''
        if alias_el is not None:
            alias = alias_el.next_sibling
        imdb_code_el = video_info.find('strong', text='IMDb编码:')
        imdb_code = ''
        if imdb_code_el is not None:
            imdb_code = imdb_code_el.next_sibling
        score_el = video_info.find('strong', text='评分:')
        score = ''
        if score_el is not None:
            score = score_el.next_sibling
        article_tags_div = video_soap.find('div', {'class': 'article-tags'})
        article_tags = article_tags_div.find_all('a')
        tags = ''
        for tag in article_tags:
            tags += tag.text + ';'
        tags = tags.rstrip(';')
        cover_picture_div = video_soap.find('div', {'class': 'video_img'})
        if cover_picture_div is not None:
            cover_picture_origin = cover_picture_div.find('img')['src']
            # img_extension_offset = cover_picture_origin.rfind('.')
            img_name_offset = cover_picture_origin.rfind('/')
            img_name = cover_picture_origin[img_name_offset + 1::]
            img_file = requests.get(cover_picture_origin).content
            # open('/Users/wayne/Pictures/91movies/' + img_name, 'wb').write(img_file)
        img_list = video_soap.find('p', {'class': 'jietu'}).find_all('img')
        for img in img_list:
            pass
            # print(img['data-original'])
        plot_introduction = video_soap.find('p', {'class': 'jianjie'}).find('span').text

        category = video_soap.find('ul', {'class': 'article-meta'}).find('a').text
        print(category)
        exit()

        # get download resources
        down_list = video_soap.find('ul', {'id': 'download-list'})
        if down_list is not None:
            li_list = down_list.find_all('li')
            for li in li_list:
                name = li.find('span').text
                e2dk_href = li.select_one("a[href*=ed2k]")
                magnet_href = li.select_one("a[href*=magnet]")
                if e2dk_href is not None:
                    e2dk = e2dk_href['href']
                if magnet_href is not None:
                    magnet = magnet_href['href']
                # print(magnet)
                exit()

    next_page = soap.find('li', {'class': 'next-page'})
    if next_page.find('a') is None:
        break
    url = next_page.find('a')['href']
