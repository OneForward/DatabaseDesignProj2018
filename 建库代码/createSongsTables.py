import pymysql.cursors
import glob
import json
import os.path as osp
all_albums = glob.glob('database_json/*all_songs.json')
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)


with connection.cursor() as cursor:
    # Create a new record
    for album_file in all_albums:
        if osp.getsize(album_file) < 1024:
            continue
        json_data = open(album_file, 'rb').read()
        data = json.loads(json_data, encoding='utf-8')
        album = data['album']
        print('album id = ', album['id'])
        for song in data['songs']:
            song_sql = "INSERT IGNORE INTO SONGS(song_id,song_name,\
                                    resource_url,style,album_id) \
                                      VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(song_sql, (song['id'], song['name'], \
                                    '', '', song['al']['id']))   
            try:
                connection.commit()
            finally:
                pass

with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT COUNT(*) FROM SONGS"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)


connection.close()