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


with connection.cursor() as cursor:
   for album_file in all_albums:
        if osp.getsize(album_file) < 1024:
            continue
        json_data = open(album_file, 'rb').read()
        data = json.loads(json_data, encoding='utf-8')
        album = data['album']
        print('album id = ', album['id']) 
        album_desc_sql = "UPDATE Albums SET description=(%s) \
                                  WHERE album_id=(%s)"
        cursor.execute(album_desc_sql, (album['description'], album['id']))   
        al_sql = "INSERT IGNORE INTO Artist_Album(artist_id, album_id) \
                      VALUES(%s, %s)"
        for artist in album['artists']:
            cursor.execute(al_sql, (artist['id'], album['id']))                                     
        for song in data['songs']:
            as_sql = "INSERT IGNORE INTO Artist_Songs(artist_id, song_id) \
                      VALUES(%s, %s)"
            for artist in song['ar']:
                cursor.execute(as_sql, (artist['id'], song['id']))      
            try:
                connection.commit()
            finally:
                pass

with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT COUNT(*) FROM ArtistAlbumSongs"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)


connection.close()