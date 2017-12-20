#!
import requests
from bs4 import BeautifulSoup

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
header = {'User-Agent':ua}


location = 'shanghai'
checkinDate='2017-12-19'
checkoutDate='2017-12-20'

def hyatt_city(location, checkinDate, checkoutDate):
    url = "https://www.hyatt.com/zh-CN/search/shanghai?location=%s&checkinDate=%s&checkoutDate=%s" % (location, checkinDate, checkoutDate)
    html = requests.get(url, headers = header, allow_redirects=False).content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('div.p-hotel-card')
    print(len(source))
    for i in range(len(source)):
        name = soup.select('div.p-hotel-card')[i].select('div.hotel-name')[0].text
        print(name)
        address = soup.select('div.p-hotel-card')[i].select('div.address-line1')[0].text
        price = soup.select('div.p-hotel-card')[i].select('div.rate')[0].text.strip()
        print(name)
        print(address)
        print(price)
        print('--------------------------------')

    
https://www.hyatt.com/zh-CN/shop/shaaz?rooms=1&adults=1&location=shanghai&checkinDate=2017-12-18&checkoutDate=2017-12-19&rate=P&kids=0
    
