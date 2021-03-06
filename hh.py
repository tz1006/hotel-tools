#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone

###############################
city_list = ['anshun', 'aomen', 'beijing', 'benxi', 'changzhou', 'chongqing', 'dandong', 'dalian', 'fuzhou', 'foshan', 'guiyang', 'guangzhou', 'geermu', 'huizhou', 'hangzhou', 'hefei', 'haikou', 'jiaxing', 'jiuzhaigou', 'jilin', 'jinan', 'linzhi', 'lijiang', 'ningbo', 'putian', 'qingdao', 'quanzhou', 'sanqingshan', 'shiyan', 'suzhou', 'shanghai', 'shenzhen', 'suzhou', 'shengyang', 'shijiazhang', 'sanya', 'tianjin', 'urumqi', 'wuxi', 'wuhu', 'wencheng', 'wuhan', 'HongKong', 'xian', 'xishuangbanna', 'xianggelila', 'xiamen', 'yantai', 'yuxi', 'zhoushan', 'zhongshan', 'zhengzhou', 'zhuzhou']

#######--sqlite3--#######

def delete_form(dbname, formname):
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS %s;" % formname)
    conn.commit()
    conn.close()
    print("Form %s Deleted!" % formname)

def create_form(dbname, formname):
    day0 = get_date(0)
    day1 = get_date(1)
    day2 = get_date(2)
    day3 = get_date(3)
    day4 = get_date(4)
    day5 = get_date(5)
    day6 = get_date(6)
    day7 = get_date(7)
    day8 = get_date(8)
    day9 = get_date(9)
    day10 = get_date(10)
    day11 = get_date(11)
    day12 = get_date(12)
    day13 = get_date(13)
    day14 = get_date(14)
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS %s
        (NAME TEXT PRIMARY KEY UNIQUE,
        CODE   TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT,
        %s  TEXT);''' % (formname, day0, day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12, day13, day14))
    conn.commit()
    conn.close()
    print("Form %s Created!" % formname)

def insert_name(dbname, formname, name, code):
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("INSERT INTO %s (NAME, CODE) VALUES (?, ?)" % formname,(name, code))
    conn.commit()
    conn.close()

def update_data(dbname, formname, code, key, value):
    key = '\'%s\'' % key
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("UPDATE %s set %s=? where CODE=?" % (formname, key), (value,code))
    conn.commit()
    conn.close()

def get_date(day=0):
    now = datetime.now(timezone('Asia/Shanghai'))
    delta = timedelta(days=day)
    date = (now + delta).strftime('%Y-%m-%d')  
    return(date)
    
    
    arrivalDate = '%s-%s-%s' % (today.year, today.month, today.day)
    departureDate = '%s-%s-%s' % (today.year, today.month, today.day+1)

##############################
def get_code(city):
    if city == 'guiyang':
        ctyhocn_code = 'KWEGUGI'
        name = '贵阳汉唐希尔顿花园酒店'
        insert_name('HH', 'PRICE', name, ctyhocn_code)
        insert_name('HH', 'POINTS', name, ctyhocn_code)
        code_list.append(ctyhocn_code)
    elif city == 'benxi':
        ctyhocn_code = 'SHEBCDI'
        name = '本溪希尔顿逸林度假酒店'
        insert_name('HH', 'PRICE', name, ctyhocn_code)
        insert_name('HH', 'POINTS', name, ctyhocn_code)
        code_list.append(ctyhocn_code)
    elif city == 'aomen':
        ctyhocn_code = 'MFMCSCI'
        name = '澳门金沙城中心康莱德酒店'
        insert_name('HH', 'PRICE', name, ctyhocn_code)
        insert_name('HH', 'POINTS', name, ctyhocn_code)
        code_list.append(ctyhocn_code)
    elif city == 'suzhou':
        pass
    else:
        ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
        header = {'User-Agent':ua_mo}
        url = 'http://www.hilton.com.cn/zh-cn/city/%s-hotels.html' % city
        html = None
        while html == None:
            html = requests.get(url, headers = header, timeout=3, allow_redirects=False).content
        hilton_soup = BeautifulSoup(html, "html.parser")
        source = hilton_soup.select('div.computer')
        for i in range(len(source)):
            name = source[i].select('span.img-wrap-name')[0].text
            if source[i].select('a.city-open') == []:
                ctyhocn_code = source[i].select('a.city-booking')[0].get('href')[-7:-1]
                code_list.append(ctyhocn_code)
            else:
                ctyhocn_code = '未开业'
            insert_name('HH', 'PRICE', name, ctyhocn_code)
            insert_name('HH', 'POINTS', name, ctyhocn_code)
        print(len(source))

def get_code_list():
    global code_list
    code_list = []
    delete_form('HH', 'PRICE')
    create_form('HH', 'PRICE')
    delete_form('HH', 'POINTS')
    create_form('HH', 'POINTS')
    for i in city_list:
        get_code(i)
    print('Finish!')

def get_price(code):
    s = requests.session()
    s.keep_alive = False
    arrivalDate = get_date(0)
    departureDate = get_date(1)
    url = 'https://secure3.hilton.com/zh_CN/hi/reservation/book.htm?ctyhocn=%s&arrivalDate=%s&departureDate=%s&hhonorsRate=false&numberOfRooms=1&inputModule=HOTEL_SEARCH&internalDeepLinking=true&toAvailCalendar=true' % (code, arrivalDate, departureDate)
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
    header = {'User-Agent':ua}
    print(url)
    html = s.get(url, headers = header).content
    hilton_soup = BeautifulSoup(html, "html.parser")
    source = hilton_soup.select('td.priceOrAvailability')
    for x in range(len(source)):
        key = 'DAY%s' % x
        if source[x].select('img') == []:
            price = source[x].strong.text
            update_data('HH', 'PRICE', code, key, price)
            print(key, price)


delete_form('HH', 'PRICE')
create_form('HH', 'PRICE')
delete_form('HH', 'POINTS')
create_form('HH', 'POINTS')
get_code_list()


for i in code_list:
    get_price(i)











