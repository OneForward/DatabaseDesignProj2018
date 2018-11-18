import pymysql.cursors
import glob
import json
import os.path as osp

all_albums = glob.glob('database_json/*all_songs.json')

for album_file in all_albums:
    if osp.getsize(album_file) < 1024:
        continue
    json_data = open(album_file, 'rb').read()
    data = json.loads(json_data, encoding='utf-8')
    album = data['album']
    print('album id = ', album['id'])
    for song in data['songs']:
        print(song['id'])
    
