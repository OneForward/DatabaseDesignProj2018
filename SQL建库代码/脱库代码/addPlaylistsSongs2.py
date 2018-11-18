import glob
import json
from utils import search
import os
import pymysql 

playlists = glob.glob('../database_json/playlist*.json')

connection = pymysql.connect(host='localhost',
                     user='root',
                     password='x',
                     db='music',
                     cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
    for playlist in playlists:
        json_data = open(playlist, 'rb').read()
        data = json.loads(json_data, encoding='utf-8')
        for song in data['playlist']['tracks']:
            # print(song)
            # parse_song_id_and_add_everything(song['id'])
            sp_sql = "INSERT INTO playlist_songs(playlist_id, song_id) \
                        VALUES (%s, %s)"
            cursor.execute(sp_sql, (data['playlist']['id'], song['id']))
        connection.commit()

    # break
       
