import json
from utils import search
import pymysql
json_data = open('top_playlists.json', 'rb').read()
data = json.loads(json_data, encoding='utf-8')

connection = pymysql.connect(host='localhost',
                     user='root',
                     password='x',
                     db='music',
                     cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
    for playlist in data['playlists']:
        # u_sql = search()
        # usr = playlist['creator']
        # u_sql = "REPLACE INTO usrs(usr_id, nickname, gender, birthday, province, city, avatar_url, signature) \
        #          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        # cursor.execute(u_sql, tuple(map(usr.get, ('userId', 'nickname', \
        #         'gender', 'birthday', 'province', 'city', 'avatarUrl', 'signature'))))
        # p_sql = "INSERT IGNORE INTO playlists(playlist_id, creator_id, playlist_pic_url, playlist_name, description, createTime, updateTime) \
        #          VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # cursor.execute(p_sql, (playlist['id'], playlist['creator']['userId'], playlist['coverImgUrl'],\
        #              playlist['name'], playlist['description'], playlist['createTime'], playlist['updateTime']) )
        search('playlist_id', playlist['id'])
connection.commit()
