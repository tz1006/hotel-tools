#!
import requests
from bs4 import BeautifulSoup

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
header = {'User-Agent':ua}


location = 'shanghai'
checkinDate='2017-12-25'
checkoutDate='2017-12-26'

def hyatt_city(location, checkinDate, checkoutDate):
    url = "https://www.hyatt.com/zh-CN/search/shanghai?location=%s&checkinDate=%s&checkoutDate=%s" % (location, checkinDate, checkoutDate)
    html = requests.get(url, headers = header, allow_redirects=False).content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('div.p-hotel-card')
    print(len(source))
    for i in range(len(source)):
        name = source[i].select('div.hotel-name')[0].text
        address = source[i].select('div.hotel-address')[0].div.text
        if source[i].select('em') == []:
            price = source[i].select('div.rate')[0].text.strip()
            href = source[i].select('a.button-shop')[0].get('href')
            code = href.split('?')[0].split('/')[2]
        else:
            price = '即将推出'
            code = None
        print(name)
        print(code)
        print(address)
        print(price)
        print('--------------------------------')

    
https://www.hyatt.com/zh-CN/shop/shaaz?rooms=1&adults=1&location=shanghai&checkinDate=2017-12-18&checkoutDate=2017-12-19&rate=P&kids=0
    
