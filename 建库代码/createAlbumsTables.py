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
        for artist_file in all_artists:
            json_data = open(artist_file, 'rb').read()
            data = json.loads(json_data, encoding='utf-8') 
            # artist = data['artist']
            # artist_desc_sql = "UPDATE ARTISTS SET briefDesc=(%s) \
            #                       WHERE artist_id=(%s)"
            # cursor.execute(artist_desc_sql, (artist['briefDesc'], artist['id']) )
            # connection.commit()
            for album in data['hotAlbums']:

                al_sql = "REPLACE INTO ALBUMS(album_id, album_name, \
                album_pic_url, publish_time, description, company, type, \
                sub_type, artist_id,  songs_count) \
                VALUES(%s, %s, %s,  %s, %s, %s,  %s, %s, %s, %s)"
                
                cursor.execute(al_sql, (album['id'], album['name'], 
                  album['picUrl'], album['publishTime'], album['description'], 
                  album['company'], album['type'], album['subType'],
                  data['artist']['id'], album['size']))  
                try:
                    connection.commit()
                finally:
                    pass

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT COUNT(*) FROM ALBUMS"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

finally:
    connection.close()