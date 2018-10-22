import os
import json
import requests
import os.path as osp
import time
import pymysql 

def search(obj, attr, save=True):
    url = 'http://localhost:3000' 
    basedir = '../database_json/'
    if not osp.exists(basedir):
        os.mkdir(basedir)
    if obj == 'search':
        url += '/search?keywords=' + str(attr)
        fname = basedir + str(attr) + '_search_rst.json'
    elif obj == 'song_id':
        url += '/song/detail?ids={}'.format(attr)
        fname = basedir + 'song_id_{}.json'.format(attr)
    elif obj == 'album_id':
        url += '/album/?id={}'.format(attr)
        fname = basedir + 'album_id_{}.json'.format(attr)  
    elif obj == 'artist_id':
        url += '/artists?id=' + str(attr)
        fname = basedir + 'artist_id_{}.json'.format(attr)  
    elif obj == 'artist_albums':
        url += '/artist/album?id={}&limit=200'.format(attr)
        fname = basedir + 'artist_id_{}_albums.json'.format(attr)
    elif obj == 'album_all_songs':
        url += '/album?id={}'.format(attr[1])
        fname = basedir + 'artist_id_{}_album_id_{}_all_songs.json'.format(attr[0], attr[1])

    else:
        return
    if not save:
        return
    if (osp.exists(fname) and osp.getsize(fname) > 800):
        return open(fname, 'rb').read()
    c = requests.get(url).content
    print(url, '\ncontentsize = {}', len(c))
    with open(fname, 'wb') as f:
        f.write(c)
    time.sleep(1)
    return c

def update_song(song):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        song_sql = "REPLACE IGNORE INTO SONGS(song_id,song_name,\
                                resource_url,style, is_hot, album_id) \
                                  VALUES(%s, %s, %s, %s, %s)"

        cursor.execute(song_sql, (song['id'], song['name'], song['url'], 
                        song['style'], song['is_hot'], song['album_id'])) 
        cursor.commit()
    connection.close()

def update_album(album):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        al_sql = "REPLACE INTO ALBUMS(album_id, album_name, \
            album_pic_url, publish_time, description, company, type, \
            sub_type, artist_id,  songs_count) \
        VALUES(%s, %s, %s,  %s, %s, %s,  %s, %s, %s, %s)"
        
        cursor.execute(al_sql, (album['id'], album['name'], 
              album['picUrl'], album['publishTime'], album['description'], 
              album['company'], album['type'], album['subType'],
              album['artist']['id'], album['size'])) 
        for song in album['songs']:
            aa_sql = "REPLACE INTO Artist_Albums(artist_id, album_id) \
                      VALUES(%s, %s)"
            cursor.execute(aa_sql, (artist['id'], album['id']))                                     
        
            as_sql = "REPLACE INTO Artist_Songs(artist_id, song_id) \
                      VALUES(%s, %s)"
            cursor.execute(as_sql, (artist['id'], song['id']))  
        cursor.commit()
    connection.close()

def update_artist(artist):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        ar_sql =  "REPLACE INTO "\
                  "ARTISTS(artist_id,artist_name, artist_pic_url, "\
                  "briefDesc, albums_count, songs_count) "\
                  "VALUES(%s, %s, %s, %s, %s, %s)"
                  
        cursor.execute(ar_sql, 
          tuple(map(artist.get, ['id', 'name', 'picUrl', 
                  'briefDesc', 'albumSize', 'musicSize']) ))
        cursor.commit()
    connection.close()

def delete(_type, _id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        if _type == DELETE_SONG:
            cursor.execute("DELETE FROM songs WHERE %s", _id)
        if _type == DELETE_ALBUM:
            cursor.execute("DELETE FROM albums WHERE %s", _id)
        if _type == DELETE_ARTIST:
            cursor.execute("DELETE FROM artists WHERE %s", _id)
        cursor.commit()
    connection.close()

def search_songs_by_song_id(song_id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:

        song_sql = "SELECT * FROM Songs WHERE song_id=%s;"
        album_sql = "SELECT * FROM Albums WHERE album_id=%s;"
        artist_sql = "SELECT * FROM Artists WHERE artist_id=%s;"
        artist_by_song_sql = "SELECT artist_id FROM Artist_Songs WHERE song_id=%s;"
        
        cursor.execute(song_sql, song_id)
        songs = cursor.fetchone()

        cursor.execute(album_sql, songs['album_id'])
        album = cursor.fetchone()

        cursor.execute(artist_by_song_sql, song_id)
        artist_ids = cursor.fetchall()
        artists = []
        for artist_id in artist_ids:
            cursor.execute(artist_sql, artist_id['artist_id'])
            artists.append(cursor.fetchone())

        songs['album'] = album 
        songs['artists'] = artists  

    connection.close()
    return {'songs': songs, 'code': 200}

def search_album_by_album_id(album_id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        album_sql = "SELECT * FROM Albums WHERE album_id=%s;"
        song_sql = "SELECT * FROM Songs WHERE song_id=%s;"
        artist_sql = "SELECT * FROM Artists WHERE artist_id=%s;"
        songs_album_sql = "SELECT * FROM Songs WHERE album_id=%s;"
        artist_by_album_sql = "SELECT artist_id FROM Artist_Album WHERE album_id=%s;"

        cursor.execute(album_sql, album_id)
        album = cursor.fetchone()

        cursor.execute(songs_album_sql, album_id)
        songs = cursor.fetchall()

        cursor.execute(artist_by_album_sql, album_id)
        artist_ids = cursor.fetchall()

        artists = []
        for artist_id in artist_ids:
            cursor.execute(artist_sql, artist_id['artist_id'])
            artists.append(cursor.fetchone())
        
        album['artists'] = artists
    connection.close() 
    return {'songs': songs, 'album': album, 'code': 200}



def search_artist_by_artist_id(artist_id):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='x',
                             db='music',
                             cursorclass=pymysql.cursors.DictCursor)
    artist_sql = "SELECT * FROM Artists WHERE artist_id=%s;"
    album_sql = "SELECT * FROM Albums WHERE album_id=%s;"
    song_sql = "SELECT * FROM Songs WHERE song_id=%s;"
    hot_songs_by_artist_sql = "SELECT * FROM Artist_Hot_Songs WHERE artist_id=%s;"
    # songs_artists_sql = "SELECT song_id FROM Artist_Songs WHERE artist_id=%s;"
    album_by_artist_sql = "SELECT album_id FROM Artist_Album WHERE artist_id=%s;"
    with connection.cursor() as cursor:
        cursor.execute(artist_sql, artist_id)
        artist = cursor.fetchone()

        cursor.execute(album_by_artist_sql, artist_id)
        album_ids = cursor.fetchall()
        
        cursor.execute(hot_songs_by_artist_sql, artist_id)
        song_ids = cursor.fetchall()

        albums = []
        for album_id in album_ids:
            cursor.execute(album_sql, album_id['album_id'])
            albums.append(cursor.fetchone())
        
        songs = []
        for song_id in song_ids:
            cursor.execute(song_sql, song_id['song_id'])
            songs.append(cursor.fetchone())
        
        # artists['hot_songs'] = songs 

    connection.close() 
    return {'artist': artist, 'hot_albums': albums, 'hot_songs': songs, 'code': 200}