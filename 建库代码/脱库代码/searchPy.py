import requests
import argparse
import os.path as osp
import os
parser = argparse.ArgumentParser(description='Search In Command')

parser.add_argument('-s', '--search', type=str, default='Momoe', 
                    help='Text / Keywords to search')
args = parser.parse_args()
    
url = 'http://localhost:3000/search?keywords=' + args.search
c = requests.get(url).content
if not osp.exists('database_json/'):
    os.mkdir('database_json/')
with open('database_json/' + args.search + '.json', 'wb') as f:
    f.write(c)
print(c)
