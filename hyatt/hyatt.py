#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: hiltoncode.py

import os
import time
import json
from pprint import pprint
from tqdm import tqdm
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from webdriver import webdriver
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


def quote_price(hotel_code, date, CUP=False):
    if CUP:
        offercode = 'CUP19'
        checkoutdate = datechange(date, 3)
    else:
        offercode = ''
        checkoutdate = datechange(date, 1)
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
    if html == None:
        price = True
        currency = None
    elif html == False:
        price = None
        currency = None
    else:
        soup = BeautifulSoup(html, "html.parser")
        #alert = soup.selector('div.m-booking-alert')
        alert = soup.find_all('div', attrs={'class':'m-booking-alert'})
        if CUP and len(alert) == 1:
            price = None
        else:
            price_soup = soup.find_all('div', attrs={'class':'b-text_weight-bold rate-pricing'})[0]
            price = int(price_soup.span.get('data-price'))
            currency = price_soup.find_all('span')[1].text
    # CUP
    if CUP:
        return price
    else:
        return price, currency



def download(date):
    data = []
    for i in tqdm(hotels_list):
        name = i['name']
        code = i['code']
        price, currency = quote_price(code, date, CUP=False)
        if price != False and price != False:
            price = int(price * 1.16)
            CUP_price = quote_price(code, date, CUP=True)
        # 税后
        if CUP_price != None and CUP_price != False:
            CUP_price = int(CUP_price * 1.16)
            Total_CUP_price = CUP_price * 3
        else:
            Total_CUP_price = CUP_price
        d = {'date': date,
             'name': name,
             'price': price,
             'CUP_price': CUP_price,
             'Total_CUP_price': Total_CUP_price,
             'currency': currency
             }
        pprint(d)
        data.append(d)
    save_json(date, data)



def save_json(date, d):
    #dir
    if not os.path.exists('data'):
        os.makedirs('data')
    # save_json
    path = 'data/%s.json' % date
    with open(path, 'w') as f:
        content = json.dumps(d)
        f.write(content)
    print(path)


if __name__ == '__main__':
    hotels_list = cn_hotels_list()
    driver = webdriver(1000, 20)
    download('2019-05-08')
    import code
    code.interact(banner="", local=locals())



#a = quote_price('jjnye','2019-05-16')

# https://www.hyatt.com/zh-CN/explore-hotels/partial?regionGroup=5-Asia&categories=&brands=
