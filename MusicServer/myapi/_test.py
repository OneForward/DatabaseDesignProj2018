import requests
import json

# type  action
# 1     parse_song_id_and_add_everything
# 2     parse_album_id_and_add_everything
data = {
    'type': 1,
    'id': 1318610318,
}

url = 'http://localhost:8000/myapi/fetchpost/'
requests.post(url, json=json.dumps(data))