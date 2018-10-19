import json
import requests
import os.path as osp
import time
def search(obj, attr, save=True):
    url = 'http://localhost:3000' 
    basedir = './database_json/'
    if obj == 'search':
        url += '/search?keywords=' + str(attr)
        fname = basedir + str(attr) + '_search_rst.json'
    elif obj == 'artist_id':
        url += '/artists?id=' + str(attr)
        fname = basedir + 'artist_id_' + str(attr) + '.json'
    elif obj == 'artist_album_id':
        url += '/artist/album?id={}&limit=200'.format(attr)
        fname = basedir + 'artist_id_{}_albums.json'.format(attr)
    elif obj == 'album_all_songs':
        url += '/album?id={}'.format(attr[1])
        fname = basedir + 'artist_id_{}_album_id_{}_all_songs.json'.format(attr[0], attr[1])
    elif obj == 'song_id':
        url += 'song/detail?ids={}'.format(attr[0])
        fname = basedir + 'song_id_{}.json'.format(attr[0])
    else:
        return
    # osp.exists(fname)

    if not save or  osp.getsize(fname) > 1024:
        return
    c = requests.get(url).content
    print(url, '\ncontentsize = {}', len(c))
    with open(fname, 'wb') as f:
        f.write(c)
    time.sleep(1)

if __name__ == '__main__':
    json_data = open('./database_json/top_artists_100.json', 'rb').read()
    data = json.loads(json_data, encoding='utf-8')

    for artist in data['artists']:
        search('artist_id', artist['id'])
        search('artist_album_id', artist['id'])
        print(artist)

