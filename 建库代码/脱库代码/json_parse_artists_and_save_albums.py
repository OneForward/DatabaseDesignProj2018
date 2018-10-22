import json
from utils import search

if __name__ == '__main__':
    json_data = open('../database_json/top_artists_100.json', 'rb').read()
    data = json.loads(json_data, encoding='utf-8')

    for artist in data['artists']:
        search('artist_id', artist['id'])
        search('artist_albums', artist['id'])
        print(artist)

