#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
import threading

###############################
city_list = ['anshun', 'aomen', 'beijing', 'benxi', 'changzhou', 'chongqing', 'dandong', 'dalian', 'fuzhou', 'foshan', 'guiyang', 'guangzhou', 'geermu', 'huizhou', 'hangzhou', 'hefei', 'haikou', 'jiaxing', 'jiuzhaigou', 'jilin', 'jinan', 'linzhi', 'lijiang', 'ningbo', 'putian', 'qingdao', 'quanzhou', 'sanqingshan', 'shiyan', 'suzhou', 'shanghai', 'shenzhen', 'suzhou', 'shengyang', 'shijiazhang', 'sanya', 'tianjin', 'urumqi', 'wuxi', 'wuhu', 'wencheng', 'wuhan', 'HongKong', 'xian', 'xishuangbanna', 'xianggelila', 'xiamen', 'yantai', 'yuxi', 'zhoushan', 'zhongshan', 'zhengzhou', 'zhuzhou']

if __name__ != '__main__':
    print('正在获取 code_list ')

#############################
# Sqlite3
def delete_form(dbname, formname):
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS %s;" % formname)
    conn.commit()
    conn.close()
    print("Form %s Deleted!" % formname)

# 创建表
def create_form(dbname, formname):
    day0 = '\'%s\'' % get_date(0)
    day1 = '\'%s\'' % get_date(1)
    day2 = '\'%s\'' % get_date(2)
    day3 = '\'%s\'' % get_date(3)
    day4 = '\'%s\'' % get_date(4)
    day5 = '\'%s\'' % get_date(5)
    day6 = '\'%s\'' % get_date(6)
    day7 = '\'%s\'' % get_date(7)
    day8 = '\'%s\'' % get_date(8)
    day9 = '\'%s\'' % get_date(9)
    day10 = '\'%s\'' % get_date(10)
    day11 = '\'%s\'' % get_date(11)
    day12 = '\'%s\'' % get_date(12)
    day13 = '\'%s\'' % get_date(13)
    day14 = '\'%s\'' % get_date(14)
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
    print("已在数据库 %s 中创建表 %s ！" % (dbname, formname))

# 插入hotelcode
def insert_name(dbname, formname, name, code):
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("INSERT INTO %s (NAME, CODE) VALUES (?, ?)" % formname,(name, code))
    conn.commit()
    conn.close()

################################
# 获取日期
def get_date(day=0):
    now = datetime.now(timezone('Asia/Shanghai'))
    delta = timedelta(days=day)
    date = (now + delta).strftime('%Y-%m-%d')  
    return(date)

s = requests.session()
s.keep_alive = False

    
def get_code(city):
    if city == 'guiyang':
        ctyhocn_code = 'KWEGUGI'
        name = '贵阳汉唐希尔顿花园酒店'
        insert_name('hilton', 'PRICE', name, ctyhocn_code)
        insert_name('hilton', 'POINTS', name, ctyhocn_code)
        code_list.append(ctyhocn_code)
    elif city == 'benxi':
        ctyhocn_code = 'SHEBCDI'
        name = '本溪希尔顿逸林度假酒店'
        insert_name('hilton', 'PRICE', name, ctyhocn_code)
        insert_name('hilton', 'POINTS', name, ctyhocn_code)
        code_list.append(ctyhocn_code)
    elif city == 'aomen':
        ctyhocn_code = 'MFMCSCI'
        name = '澳门金沙城中心康莱德酒店'
        insert_name('hilton', 'PRICE', name, ctyhocn_code)
        insert_name('hilton', 'POINTS', name, ctyhocn_code)
        code_list.append(ctyhocn_code)
    elif city == 'suzhou':
        pass
    else:
        url = 'http://www.hilton.com.cn/zh-cn/city/%s-hotels.html' % city
        r = None
        while r == None:
            r = s.get(url, timeout=7, allow_redirects=False)
        print(r.status_code)
        html = r.content
        hilton_soup = BeautifulSoup(html, "html.parser")
        source = hilton_soup.select('div.computer')
        for i in range(len(source)):
            name = source[i].select('span.img-wrap-name')[0].text
            if source[i].select('a.city-open') == []:
                ctyhocn_code = source[i].select('a.city-booking')[0].get('href')[-7:-1]
                code_list.append(ctyhocn_code)
            else:
                ctyhocn_code = '未开业'
            insert_name('hilton', 'PRICE', name, ctyhocn_code)
            insert_name('hilton', 'POINTS', name, ctyhocn_code)
        print(len(source))

def get_code_list(dbname):
    global code_list
    code_list = []
    delete_form(dbname, 'PRICE')
    delete_form(dbname, 'POINTS')
    create_form(dbname, 'PRICE')
    create_form(dbname, 'POINTS')
    threads = []
    for city in city_list:
        a = threading.Thread(target=get_code, args=(city,))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()


get_code_list('hilton')

print('成功载入%s个酒店代码到code_list并写入数据库 hilton.db' % len(code_list))



