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