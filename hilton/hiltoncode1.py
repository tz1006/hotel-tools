#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import requests
import sqlite3
from bs4 import BeautifulSoup

###############################
city_list = ['anshun', 'aomen', 'beijing', 'benxi', 'changzhou', 'chongqing', 'dandong', 'dalian', 'fuzhou', 'foshan', 'guiyang', 'guangzhou', 'geermu', 'huizhou', 'hangzhou', 'hefei', 'haikou', 'jiaxing', 'jiuzhaigou', 'jilin', 'jinan', 'linzhi', 'lijiang', 'ningbo', 'putian', 'qingdao', 'quanzhou', 'sanqingshan', 'shiyan', 'suzhou', 'shanghai', 'shenzhen', 'shengyang', 'shijiazhang', 'sanya', 'tianjin', 'urumqi', 'wuxi', 'wuhu', 'wencheng', 'wuhan', 'HongKong', 'xian', 'xishuangbanna', 'xianggelila', 'xiamen', 'yantai', 'yuxi', 'zhoushan', 'zhongshan', 'zhengzhou', 'zhuzhou']

s = requests.session
s.keep_alive = False

#######--sqlite3--#######

def delete_form(dbname, formname):
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS %s;" % formname)
    conn.commit()
    conn.close()
    print("Form %s Deleted!" % formname)

#########################
# 获取中国酒店 ctyhocn_code

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
