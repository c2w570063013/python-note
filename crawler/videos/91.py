import requests
from bs4 import BeautifulSoup
import info
from datetime import datetime

# turn pages
while True:
    print('scraping ' + info.url)
    s = requests.Session()
    r = s.get(info.url, headers=info.headers).text
    soap = BeautifulSoup(r, 'html5lib')
    info_list = soap.find_all('article', {'class': 'u-movie'})
    # traverse current page for getting videos links
    for i in info_list:
        video_page = i.find('a')['href']
        # html5lib html.parser
        video_soap = BeautifulSoup(s.get(video_page).text, 'html5lib')
        title = video_soap.find('h1', {'class': 'article-title'}).find('a').text.rstrip('在线观看')
        name_el = i.find('h2').text
        name = name_el
        season_cn = ''
        if name_el.find(' ') > 0:
            name = name_el[:name_el.find(' ')]
            season_cn = name_el[name_el.rfind(' ') + 1::]
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
        debut_area = ''
        if debut_date_el is not None:
            debut = debut_date_el.next_sibling
            l_bracket = debut.find('(')
            r_bracket = debut.find(')')
            debut_date = debut
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
        cover_picture = ''
        cover_picture_origin = ''
        if cover_picture_div is not None:
            cover_picture_origin = cover_picture_div.find('img')['src']
            # img_extension_offset = cover_picture_origin.rfind('.')
            img_name_offset = cover_picture_origin.rfind('/')
            img_name = cover_picture_origin[img_name_offset + 1::]
            cover_picture = img_name
            img_file = requests.get(cover_picture_origin).content
            # open(info.cover_path + img_name, 'wb').write(img_file)
        img_list = video_soap.find('p', {'class': 'jietu'})
        if img_list is not None:
            for img in img_list.find_all('img'):
                print(img)
            exit()
            # print(img['data-original'])
        plot_introduction = video_soap.find('p', {'class': 'jianjie'}).find('span').text

        category = video_soap.find('ul', {'class': 'article-meta'}).find('a').text
        sql_category_id = "select id from tv_categories where category_name='%s'" % category.rstrip('片')
        connection = info.connect_db()
        cursor = connection.cursor()
        cursor.execute(sql_category_id)
        cat_id = cursor.fetchone()

        # get download resources
        down_list = video_soap.find('ul', {'id': 'download-list'})
        if down_list is not None:
            li_list = down_list.find_all('li')
            date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            sql_series = "insert into " \
                         "tv_series " \
                         "(" \
                         "title, name, director, scriptwriter, cast, " \
                         "category, category_id, tags, area, language, debut_date, " \
                         "debut_area, season, season_cn, episode_num, updated_episode_num, " \
                         "episode_time, alias, imdb_code, score, plot_introduction, " \
                         "cover_picture, cover_picture_origin, created_at, updated_at) values (" \
                         "'%s', '%s', '%s', '%s', '%s'," \
                         " '%s', %d, '%s', '%s', '%s', '%s', " \
                         "'%s', %d, '%s', %d, %d, " \
                         "'%s', '%s', '%s', '%s', '%s'," \
                         " '%s', '%s', '%s', '%s')" % \
                         (title, name, director.lstrip(' '), scriptwriter.lstrip(' '), cast.lstrip(' '), category,
                          cat_id[0], tags, area.lstrip(' '), language.lstrip(' '),
                          debut_date.lstrip(' '), debut_area.lstrip(' '), int(season), season_cn, int(episode_num),
                          len(li_list), episode_time.lstrip(' '),
                          alias.lstrip(' '), imdb_code.lstrip(' '), score.lstrip(' '), plot_introduction, cover_picture,
                          cover_picture_origin, date_time, date_time)
            res = cursor.execute(sql_series)
            connection.commit()
            for li in li_list:
                name = li.find('span').text
                e2dk_href = li.select_one("a[href*=ed2k]")
                magnet_href = li.select_one("a[href*=magnet]")
                if e2dk_href is not None:
                    e2dk = e2dk_href['href']
                if magnet_href is not None:
                    magnet = magnet_href['href']

    next_page = soap.find('li', {'class': 'next-page'})
    if next_page.find('a') is None:
        break
    url = next_page.find('a')['href']
