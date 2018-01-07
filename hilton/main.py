#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: hiltoncode.py

import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
import threading

from hiltoncode import code_list

s = requests.session()
s.keep_alive = False

###################################
# Sqlite3
def update_data(dbname, formname, code, key, value):
    key = '\'%s\'' % key
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("UPDATE %s set %s=? where CODE=?" % (formname, key), (value,code))
    conn.commit()
    conn.close()

# 获取日期
def get_date(day=0):
    now = datetime.now(timezone('Asia/Shanghai'))
    delta = timedelta(days=day)
    date = (now + delta).strftime('%Y-%m-%d')  
    return(date)

# 获取价格
def get_price(code):
    arrivalDate = get_date(0)
    departureDate = get_date(1)
    url = 'https://secure3.hilton.com/zh_CN/hi/reservation/book.htm?ctyhocn=%s&arrivalDate=%s&departureDate=%s&hhonorsRate=false&numberOfRooms=1&inputModule=HOTEL_SEARCH&internalDeepLinking=true&toAvailCalendar=true' % (code, arrivalDate, departureDate)
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=40)
        except:
            print('fail %s' % code)
    html = r.content
    hilton_soup = BeautifulSoup(html, "html.parser")
    source = hilton_soup.select('td.priceOrAvailability')
    #print(len(source))
    for x in range(len(source)):
        key = get_date(x)
        if source[x].select('img') == []:
            price = source[x].strong.text
            update_data('hilton', 'PRICE', code, key, price)
            #print(key, price)
    print('写入 %s ' % code)

threads = []
for i in code_list:
    a = threading.Thread(target=get_price ,args=(i,))
    threads.append(a)
    a.start()
    #print('add'+i)

