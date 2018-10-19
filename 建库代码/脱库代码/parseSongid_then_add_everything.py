import argparse
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
    elif obj == 'artist_album_id':
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


parser = argparse.ArgumentParser(description='Add everything related to certain song id in command')

parser.add_argument('-i', '--songid', type=str, default='1318610318', 
                    help='Song id to search')
args = parser.parse_args()

# get song
song_json = search("song_id", args.songid)
song_data = json.loads(song_json, encoding='utf-8')
song = song_data['songs'][0]
artists = song['ar'] # possibly multiple artists
album_id  = song['al']['id']

# get album, artists
album_json = search("album_id", album_id)
album_data = json.loads(album_json, encoding='utf-8')

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
        
        # connection.commit()
    
    # insert album to sql
    album = album_data['album']
    al_sql = "REPLACE INTO ALBUMS(album_id, album_name, \
    album_pic_url, publish_time, description, company, type, \
    sub_type, artist_id,  songs_count) \
    VALUES(%s, %s, %s,  %s, %s, %s,  %s, %s, %s, %s)"
    
    cursor.execute(al_sql, (album['id'], album['name'], 
      album['picUrl'], album['publishTime'], album['description'], 
      album['company'], album['type'], album['subType'],
      album['artist']['id'], album['size']))  
            
    # connection.commit()

    # insert song to sql
    song_sql = "INSERT IGNORE INTO SONGS(song_id,song_name,\
                                    resource_url,style,album_id) \
                                      VALUES(%s, %s, %s, %s, %s)"
    cursor.execute(song_sql, (song['id'], song['name'], \
                                    '', '', song['al']['id']))  
    # connection.commit() 

    # insert album-artist-songs
    # album_desc_sql = "UPDATE Albums SET description=(%s) \
    #                               WHERE album_id=(%s)"
    # cursor.execute(album_desc_sql, (album['description'], album['id']))   

    for artist in album['artists']:
        al_sql = "INSERT IGNORE INTO Artist_Albums(artist_id, album_id) \
                  VALUES(%s, %s)"
        cursor.execute(al_sql, (artist['id'], album['id']))                                     
    
        as_sql = "INSERT IGNORE INTO Artist_Songs(artist_id, song_id) \
                  VALUES(%s, %s) "
        cursor.execute(as_sql, (artist['id'], song['id']))      
        # connection.commit()

    for artist_data in artists_data:
        if song['id'] in (artist_data['hotSongs'][i]['id'] for i in range(len(artist_data['hotSongs']))):
            break
        song_hot_sql = "UPDATE SONGS SET is_hot=(%s) \
                          WHERE song_id=(%s)"
        cursor.execute(song_hot_sql, (1, song['id']) )
        artist_hot_song_sql = "REPLACE INTO Artist_Hot_Songs(artist_id, song_id) \
                                VALUES (%s, %s)"
        # print(artist_hot_song_sql % (artist['id'], song['id']))
        cursor.execute(artist_hot_song_sql, (artist['id'], song['id']) )
    connection.commit()


    # Test Validity
    sql = "SELECT * FROM SONGS WHERE song_id=(%s)"
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

    sql = "SELECT * FROM Artist_Albums WHERE artist_id=(%s)"
    for artist_data in artists_data:
        artist =  artist_data['artist']
        cursor.execute(sql, artist['id'])
        result = cursor.fetchall()
        print('artist_albums:\n', result)

    sql = "SELECT * FROM Artist_Songs WHERE artist_id=(%s)"
    for artist_data in artists_data:
        artist =  artist_data['artist']
        cursor.execute(sql, artist['id'])
        result = cursor.fetchall()
        print('artist_songs:\n', result)

        sql = "SELECT * FROM Artist_Hot_Songs WHERE artist_id=(%s)"
    for artist_data in artists_data:
        artist =  artist_data['artist']
        cursor.execute(sql, artist['id'])
        result = cursor.fetchall()
        print('artist_hot_songs:\n', result)
connection.close()