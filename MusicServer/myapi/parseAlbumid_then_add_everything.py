import argparse
import json
import pymysql 
from .utils import search

def parse_album_id_and_add_everything(albumid):
    # get album
    album_json = search("album_id", albumid)
    album_data = json.loads(album_json, encoding='utf-8')
    album = album_data['album']
    album_id  = album['id']

    # get songs
    songs_data = []
    for song_in_album in album_data['songs']:
        song_id = song_in_album['id']
        song_json = search("song_id", song_id)
        songs_data.append(json.loads(song_json, encoding='utf-8'))

    # get artists
    artists = album['artists'] # possibly multiple artists
    artists_data = []
    for artist in artists:
        artist_json = search("artist_id", artist['id'])
        artists_data.append(json.loads(artist_json, encoding='utf-8'))


    # mysql connection
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='x',
                                 db='music',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # insert artists to sql
        for artist_data in artists_data:
            artist =  artist_data['artist']
            ar_sql =  "INSERT IGNORE INTO "\
                      "ARTISTS(artist_id,artist_name, artist_pic_url, "\
                      "briefDesc, albums_count, songs_count) "\
                      "VALUES(%s, %s, %s, %s, %s, %s)"
                      
            cursor.execute(ar_sql, 
              tuple(map(artist.get, ['id', 'name', 'picUrl', 
                      'briefDesc', 'albumSize', 'musicSize']) ))
            
        
        # insert album to sql
        al_sql = "INSERT INTO ALBUMS(album_id, album_name, \
        album_pic_url, publish_time, description, company, type, \
        sub_type, artist_id,  songs_count) \
        VALUES(%s, %s, %s,  %s, %s, %s,  %s, %s, %s, %s)"
        
        cursor.execute(al_sql, (album['id'], album['name'], 
          album['picUrl'], album['publishTime'], album['description'], 
          album['company'], album['type'], album['subType'],
          album['artist']['id'], album['size']))  
                

        # insert song to sql
        for song_data in songs_data:
            song = song_data['songs'][0]
            song_sql = "INSERT IGNORE INTO SONGS(song_id,song_name,\
                                            resource_url,style,album_id) \
                                              VALUES(%s, %s, %s, %s, %s)"
            # print(song)
            cursor.execute(song_sql, (song['id'], song['name'], \
                                            '', '', song['al']['id']))  


        # insert album-artist-songs 
        for artist in album['artists']:
            for song_data in songs_data:
                song = song_data['songs'][0]
                al_sql = "INSERT IGNORE INTO Artist_Albums(artist_id, album_id) \
                          VALUES(%s, %s)"
                cursor.execute(al_sql, (artist['id'], album['id']))                                     
        
        for song_data in songs_data:
            song = song_data['songs'][0]
            for artist in song['ar']:
                as_sql = "INSERT IGNORE INTO Artist_Songs(artist_id, song_id) \
                          VALUES(%s, %s) "
                cursor.execute(as_sql, (artist['id'], song['id']))      


        for artist_data in artists_data:
            for song_data in songs_data:
                song = song_data['songs'][0]
                if song['id'] in (artist_data['hotSongs'][i]['id'] for i in range(len(artist_data['hotSongs']))):
                    break
                song_hot_sql = "UPDATE SONGS SET is_hot=(%s) \
                                  WHERE song_id=(%s)"
                cursor.execute(song_hot_sql, (1, song['id']) )
                artist_hot_song_sql = "INSERT IGNORE INTO Artist_Hot_Songs(artist_id, song_id) \
                                        VALUES (%s, %s)"
                cursor.execute(artist_hot_song_sql, (artist['id'], song['id']) )
        connection.commit()


        # Test Validity
        sql = "SELECT * FROM SONGS WHERE song_id=(%s)"
        for song_data in songs_data:
            song = song_data['songs'][0]
            cursor.execute(sql, song['id'])
            result = cursor.fetchall()
            print('song:\n', result)

        sql = "SELECT * FROM ALBUMS WHERE album_id=(%s)"
        cursor.execute(sql, album['id'])
        result = cursor.fetchall()
        print('album:\n', result)

        sql = "SELECT * FROM ARTISTS WHERE artist_id=(%s)"
        for artist_data in artists_data:
            artist =  artist_data['artist']
            cursor.execute(sql, artist['id'])
            result = cursor.fetchall()
            print('artist:\n', result)

        sql = "SELECT * FROM Artist_Albums WHERE artist_id=(%s) and album_id=(%s)"
        for artist_data in artists_data:
            artist =  artist_data['artist']
            cursor.execute(sql, (artist['id'], album['id']))
            result = cursor.fetchall()
            print('artist_albums:\n', result)

        sql = "SELECT * FROM Artist_Songs WHERE artist_id=(%s) and song_id=(%s)"
        for artist_data in artists_data:
            for song_data in songs_data:
                song = song_data['songs'][0]
                artist =  artist_data['artist']
                cursor.execute(sql, (artist['id'], song['id']))
                result = cursor.fetchall()
                print('artist_songs:\n', result)

            sql = "SELECT * FROM Artist_Hot_Songs WHERE artist_id=(%s) and song_id=(%s)"
        for artist_data in artists_data:
            for song_data in songs_data:
                song = song_data['songs'][0]
                artist =  artist_data['artist']
                cursor.execute(sql, (artist['id'], song['id']))
                result = cursor.fetchall()
                print('artist_songs:\n', result)
    connection.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add everything related to certain song id in command')

    parser.add_argument('-a', '--albumid', type=str, default='73845378', 
                        help='Album id to search')
    args = parser.parse_args()
    parse_album_id_and_add_everything(args.albumid)