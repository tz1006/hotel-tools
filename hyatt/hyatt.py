
#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: hiltoncode.py

import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from webdriver import webdriver
driver = webdriver(15)
#driver = webdriver.Chrome('./chromedriver')
#js = r"Object.defineProperty(navigator, 'webdriver', {get: () => undefined,});"                           
#driver.execute_script(js)



def datechange(date, change):
    change = int(change)
    date = datetime.strptime(date, '%Y-%m-%d').date()
    new_date = date + timedelta(days=change)
    new_date_string = new_date.strftime('%Y-%m-%d')
    return new_date_string





def get_cn_hotels():
    # 生成url
    url = 'https://www.hyatt.com/zh-CN/explore-hotels/partial?'
    payload = {'regionGroup': '5-Asia',
               'categories': '',
               'brands': ''}
    url += urlencode(payload)
    #print(url)
    # soup
    with requests.session() as s:
        r = s.get(url)
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    cn_soup = soup.find_all('li', attrs={'data-js-country':'大中华地区'})[0]
    cn_hotels = cn_soup.find_all('li', attrs={'class':'property b-mb2'})
    return cn_hotels


def cn_hotels_list():
    cn_hotels = get_cn_hotels()
    hotel_list = []
    for i in cn_hotels:
        name = i.a.text
        code = i.get('data-js-property')
        link = i.a.get('href')
        span = i.a.span
        if span == None:
            tag = ''
        else:
            tag = span.text
        d = {'name': name,
             'code': code,
             'link': link,
             'tag': tag}
        hotel_list.append(d)
    return hotel_list


def quote_price(hotel_code, date, promo=False):
    change = 1
    offercode = ''
    if promo:
        offercode = 'CUP19'
        change = 3
    checkoutdate = datechange(date, change)
    # url
    url = 'https://www.hyatt.com/zh-CN/shop/rates/%s?' % hotel_code
    payload = {'rooms': 1,
               'adults': 1,
               'checkinDate': date,
               'checkoutDate': checkoutdate,
               'kids': 0,
               'offercode': offercode,
               'rateFilter': 'standard'}
    url += urlencode(payload)
    #print(url)
    # soup
    html = driver.get_page(url)
    soup = BeautifulSoup(html, "html.parser")
    lowest_price_soup = soup.find_all('div', attrs={'class':'b-text_weight-bold rate-pricing'})[0]
    lowest_price = lowest_price_soup.span.get('data-price')
    return lowest_price




l = cn_hotels_list()

for i in l:
    name = i['name']
    code = i['code']
    try:
        price = quote_price(code, '2019-05-08', promo=True)
        print(price, name)
    except:
        print('None', name)
    time.sleep(0)

 


#a = quote_price('jjnye','2019-05-16')
