import glob
import json
from utils import search
import os
from parseSongid_then_add_everything_2 import parse_song_id_and_add_everything
playlists = glob.glob('../database_json/playlist*.json')

for playlist in playlists:
    json_data = open(playlist, 'rb').read()
    data = json.loads(json_data, encoding='utf-8')
    for song in data['playlist']['tracks']:
        print(song)
        try:
            parse_song_id_and_add_everything(song['id'])
        except:
            pass
        
        # break
    # break
       
