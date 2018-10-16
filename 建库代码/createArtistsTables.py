import pymysql.cursors
import glob
import json
import os.path as osp
all_albums = glob.glob('database_json/*all_songs.json')
all_artists = glob.glob('database_json/*albums.json')
top_artists = glob.glob('database_json/top_artists_100.json')
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        for artist_file in top_artists:
            json_data = open(artist_file, 'rb').read()
            data = json.loads(json_data, encoding='utf-8')
            for artist in data['artists']:
                ar_sql = "INSERT IGNORE INTO ARTISTS(artist_id,artist_name,\
                artist_pic_url, briefDesc, albums_count, songs_count) \
                                          VALUES(%s, %s, %s, %s, %s, %s)"
                cursor.execute(ar_sql, (artist['id'], artist['name'], 
                  artist['picUrl'], artist['briefDesc'], artist['albumSize'], 
                  artist['musicSize'])) 
                try:
                    connection.commit()
                finally:
                    pass

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM ARTISTS"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

finally:
    connection.close()