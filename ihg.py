#!

import requests
from bs4 import BeautifulSoup
import yaml

def query(key):
    query_url = 'https://www.ihg.com/guestapi/v1/ihg/cn/zh/web/suggestions?country=cn&language=zh&brand=ihg&query=%s' % key
    query_str = requests.get(query_url, headers = header, allow_redirects=False).content.decode(encoding ='utf-8')
    query_dict = yaml.load(query_str)
    print('-----------Result Cities------------')
    hotels = []
    for i in range(0, query_dict['preFilterCount']):
        print(query_dict['filteredSuggestionList'][i]['label'])
        hotels.append(query_dict['filteredSuggestionList'][i]['label'])
    # return hotels

