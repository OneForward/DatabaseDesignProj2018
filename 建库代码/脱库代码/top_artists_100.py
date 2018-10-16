import requests

url = 'http://localhost:3000/top/artists?offset=0&limit=100'
c = requests.get(url).content
with open('./database_json/top_artists_1000.json', 'wb') as f:
    f.write(c)