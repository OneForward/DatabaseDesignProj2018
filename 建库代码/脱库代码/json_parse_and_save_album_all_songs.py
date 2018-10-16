import glob
import json
import requests
import os.path as osp
from json_parse_and_save import search

artists = glob.glob('database_json/artist*albums.json')

for artist in artists:
    json_data = open(artist, 'rb').read()
    data = json.loads(json_data, encoding='utf-8')
    for album in data['hotAlbums']:
        print(album['id'])
        search('album_all_songs', (data['artist']['id'], album['id']))
    # break
