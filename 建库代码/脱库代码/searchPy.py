import argparse
from utils import search 

parser = argparse.ArgumentParser(description='Search In Command')

parser.add_argument('-s', '--search', type=str, default='Momoe', 
                    help='Text / Keywords to search')
args = parser.parse_args()
    
json_data = search("search", args.search)
print(json_data)

