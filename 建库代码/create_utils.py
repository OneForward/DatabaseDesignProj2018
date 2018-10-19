import pymysql.cursors
import glob
import json
import os.path as osp
all_albums = glob.glob('database_json/*all_songs.json')
all_artists = glob.glob('database_json/*albums.json')
all_artists2 = glob.glob('database_json/artist_id_*[!s].json')
top_artists = glob.glob('database_json/top_artists_100.json')
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
    # Create a new record
    # drop_table_sql = "DELETE FROM Artist_Hot_Songs"
    # cursor.execute(drop_table_sql)
    for artist_file in all_artists2:
        json_data = open(artist_file, 'rb').read()
        data = json.loads(json_data, encoding='utf-8') 
        artist = data['artist']
        artist_desc_sql = "UPDATE ARTISTS SET briefDesc=(%s) \
                              WHERE artist_id=(%s)"

        # print(artist_desc_sql % (artist['briefDesc'], artist['id']) )
        cursor.execute(artist_desc_sql, (artist['briefDesc'], artist['id']) )
        connection.commit()

        for song in data['hotSongs']:
            song_hot_sql = "UPDATE SONGS SET is_hot=(%s) \
                              WHERE song_id=(%s)"
            cursor.execute(song_hot_sql, (1, song['id']) )
            artist_hot_song_sql = "INSERT IGNORE INTO Artist_Hot_Songs(artist_id, song_id) \
                                    VALUES (%s, %s)"
            # print(artist_hot_song_sql % (artist['id'], song['id']))
            cursor.execute(artist_hot_song_sql, (artist['id'], song['id']) )
            connection.commit()
            
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM SONGS"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)