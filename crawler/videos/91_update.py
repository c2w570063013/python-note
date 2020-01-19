import requests
from bs4 import BeautifulSoup
import info
from datetime import datetime

url = info.url_update
# turn pages
while True:
    try:
        # print('scraping ' + url)
        s = requests.Session()
        r = s.get(url, headers=info.headers).text
        soap = BeautifulSoup(r, 'html5lib')
        info_list = soap.find_all('article', {'class': 'u-movie'})
        # traverse current page for getting videos links
        for i in info_list:
            try:
                # initial mysql connection
                connection = info.connect_db()
                cursor = connection.cursor()
                date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

                video_page = i.find('a')['href']
                video_soap = BeautifulSoup(s.get(video_page).text, 'html5lib')
                try:
                    last_update_time = video_soap.find('ul', {'class': 'article-meta'}).find_all('li')[1].text[
                                       :10] + ' 00:00:00'
                except Exception as e:
                    last_update_time = '2020-01-01 00:00:00'
                    info.logger("url: " + url + "\n" + str(e))
                    print(e)
                title = video_soap.find('h1', {'class': 'article-title'}).find('a').text.rstrip('在线观看')
                sql_check = "select * from tv_series where title='%s'" % title
                cursor.execute(sql_check)
                if cursor.fetchone() is not None:
                    print(date_time+' no new updated moves')
                    exit()
                name_el = i.find('h2').text
                name = name_el
                print('scraping name:' + name)
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
                official_site_el = video_info.find('strong', '官方网站:')
                official_site = ''
                if official_site_el is not None:
                    official_site = official_site_el.next_sibling
                area_el = video_info.find('strong', text='国家/地区:')
                area = ''
                if area_el is not None:
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
                    if type(l_bracket) is int and l_bracket > 1:
                        # if int(l_bracket) > 1:
                        debut_date = debut[:l_bracket]
                        debut_area = debut[l_bracket + 1:r_bracket]
                season_el = video_info.find('strong', text='季数:')
                season = 1
                if season_el is not None:
                    season = season_el.next_sibling
                episode_num_el = video_info.find('strong', text='集数:')
                episode_num = 0
                if episode_num_el is not None:
                    episode_num = episode_num_el.next_sibling
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
                    score = score_el.next_sibling if score_el.next_sibling is not None else ''
                article_tags_div = video_soap.find('div', {'class': 'article-tags'})
                article_tags = article_tags_div.find_all('a')
                tags = ''
                tags_id = []
                for tag in article_tags:
                    tag_sql_query = "select id from series_tags where name='%s'" % tag.text
                    cursor.execute(tag_sql_query)
                    res = cursor.fetchone()
                    if res is None:
                        sql_insert_tag = "insert into series_tags (name, status, created_at, updated_at) values ('%s', %d, '%s', '%s')" % (
                            tag.text, 1, date_time, date_time)
                        cursor.execute(sql_insert_tag)
                        connection.commit()
                        tags_id.append(cursor.lastrowid)
                    else:
                        # tags_id = res[0]
                        tags_id.append(res[0])
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
                    # try:
                    #     img_file = requests.get(cover_picture_origin).content
                    #     open(info.cover_path + img_name, 'wb').write(img_file)
                    # except Exception as e:
                    #     print(e)
                plot_introduction = video_soap.find('p', {'class': 'jianjie'}).find('span').text.replace('"', '\\\"')

                category = video_soap.find('ul', {'class': 'article-meta'}).find('a').text
                sql_category_id = "select id from tv_categories where category_name='%s'" % category.rstrip('片')
                cursor.execute(sql_category_id)
                cat_id = cursor.fetchone()
                cat_id_ = 12
                if cat_id is not None:
                    cat_id_ = cat_id[0]

                # get download resources
                down_list = video_soap.find('ul', {'id': 'download-list'})
                li_list = []
                if down_list is not None:
                    li_list = down_list.find_all('li')

                sql_series = 'insert into tv_series(update_time, official_site, title, name, director, scriptwriter, cast,category, category_id, tags, area, language, debut_date,debut_area, season, season_cn, episode_num, updated_episode_num,episode_time, alias, imdb_code, score, plot_introduction,cover_picture, cover_picture_origin, created_at, updated_at) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s","%s", %d, "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s")' % (
                    last_update_time, official_site, title, name, str(director), str(scriptwriter),
                    str(cast), category, cat_id_, tags,
                    str(area), str(language), str(debut_date), str(debut_area), str(season),
                    str(season_cn), str(episode_num), len(li_list), str(episode_time), str(alias),
                    str(imdb_code), str(score), plot_introduction, cover_picture, cover_picture_origin,
                    str(date_time),
                    date_time)
                cursor.execute(sql_series)
                connection.commit()
                series_id = cursor.lastrowid

                # insert series-tag relationship
                for tag_id in tags_id:
                    tag_relationship_sql = "insert into tags_relationship (tag_id, series_id, created_at, updated_at) values (%d, %d, '%s', '%s')" % (
                        tag_id, series_id, date_time, date_time)
                    cursor.execute(tag_relationship_sql)
                    connection.commit()
                for li in li_list:
                    name = li.find('span').text
                    e2dk_href = li.select_one("a[href*=ed2k]")
                    magnet_href = li.select_one("a[href*=magnet]")
                    if e2dk_href is not None:
                        e2dk = e2dk_href['href']
                    if magnet_href is not None:
                        magnet = magnet_href['href']
                    sql_episode = 'insert into tv_episode (tv_series_id, name, e2k, magnet, created_at, updated_at) values(%d, "%s", "%s", "%s", "%s", "%s")' % (
                        series_id, name, e2dk, magnet, date_time, date_time)
                    cursor.execute(sql_episode)
                    connection.commit()

                img_list = video_soap.find('p', {'class': 'jietu'})
                if img_list is not None:
                    for img in img_list.find_all('img'):
                        img_name_offset = img['data-original'].rfind('/')
                        img_name = img['data-original'][img_name_offset + 1::]
                        sql_img = "insert into tv_series_img (tv_series_id, link, origin_link, created_at, updated_at) values (%d, '%s', '%s', '%s', '%s')" % (
                            series_id, img_name, img['data-original'], date_time, date_time)
                        cursor.execute(sql_img)
                        connection.commit()
                # try:
                #     img_file = requests.get(img['data-original']).content
                #     open(info.plot_img_path + img_name, 'wb').write(img_file)
                # except Exception as e:
                #     pass
                #     print(e)
            except Exception as ee:
                print('name:' + name + ' url:' + video_page + ' ' + str(ee))
                info.logger('name:' + name + ' url:' + url + ' ' + str(ee))
        next_page = soap.find('li', {'class': 'next-page'})
        if next_page.find('a') is None:
            break
        url = next_page.find('a')['href']
    except Exception as e:
        print('name:' + name + ' url:' + url + ' ' + str(e))
        info.logger('name:' + name + "\n url: " + url + "\n" + str(e))
