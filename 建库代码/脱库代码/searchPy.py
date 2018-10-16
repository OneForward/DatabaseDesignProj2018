import requests
import argparse

parser = argparse.ArgumentParser(description='Search In Command')

parser.add_argument('-s', '--search', type=str, default='Momoe', 
                    help='Text / Keywords to search')
args = parser.parse_args()
    
url = 'http://localhost:3000/search?keywords=' + args.search
c = requests.get(url).content
with open('./database_json/' + args.search + '.json', 'wb') as f:
    f.write(c)