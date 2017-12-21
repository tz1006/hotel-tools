import requests
from bs4 import BeautifulSoup
import sqlite3
import threading

ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
header = {'User-Agent':ua_mo}

city_list = ['anshun', 'aomen', 'beijing', 'benxi', 'changzhou', 'chongqing', 'dandong', 'dalian', 'fuzhou', 'foshan', 'guiyang', 'guangzhou', 'geermu', 'huizhou', 'hangzhou', 'hefei', 'haikou', 'jiaxing', 'jiuzhaigou', 'jilin', 'jinan', 'linzhi', 'lijiang', 'ningbo', 'putian', 'qingdao', 'quanzhou', 'sanqingshan', 'shiyan', 'suzhou', 'shanghai', 'shenzhen', 'suzhou', 'shengyang', 'shijiazhang', 'sanya', 'tianjin', 'urumqi', 'wuxi', 'wuhu', 'wencheng', 'wuhan', 'HongKong', 'xian', 'xishuangbanna', 'xianggelila', 'xiamen', 'yantai', 'yuxi', 'zhoushan', 'zhongshan', 'zhengzhou', 'zhuzhou']


def get_code(city):
    globals()[city] = []
    if city == 'guiyang':
        ctyhocn_code = 'KWEGUGI'
        name = '贵阳汉唐希尔顿花园酒店'
        insert_data(ctyhocn_code, name)
    elif city == 'benxi':
        ctyhocn_code = 'SHEBCDI'
        name = '本溪希尔顿逸林度假酒店'
        insert_data(ctyhocn_code, name)
    elif city == 'aomen':
        ctyhocn_code = 'MFMCSCI'
        name = '澳门金沙城中心康莱德酒店'
        insert_data(ctyhocn_code, name)
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
            else:
                ctyhocn_code = '未开业'
            insert_data(ctyhocn_code, name)
            #ctyhocn.append(ctyhocn_code)
            #globals()[city].append(ctyhocn_code)
        #globals()[city] = list(set(globals()[city]))
        print(len(source))

def delete_form(form):
    conn = sqlite3.connect('database/hilton.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS %s;" % form)
    conn.commit()
    conn.close()
    print("%s Deleted!" % form)

def create_form(form):
    conn = sqlite3.connect('database/hilton.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS %s
        (NAME TEXT PRIMARY KEY UNIQUE,
        ID   TEXT  );''' % form)
    print("Table created successfully")
    conn.commit()
    conn.close()
    print("%s Created!" % form)

def insert_data(id, name):
    conn = sqlite3.connect('database/hilton.db')
    c = conn.cursor()
    c.execute("INSERT INTO HILTON (ID, NAME) VALUES (?, ?)",(id, name))
    conn.commit()
    conn.close()


delete_form('HILTON')
create_form('HILTON')

for i in city_list:
    print(i)
    get_code(i)
    print('finish')


def load_hilton():
    threads = []
    for i in city_list:
        a = threading.Thread(target=get_code, args=(i,))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()
    print('Load ALL')

load_hilton()

for i in city_list:
    print(i)
    get_code(i)



ctyhocn_list = {}
ctyhocn = []
def load_hilton():
    threads = []
    for i in city_list:
        a = threading.Thread(target=get_ctghocn, args=(i,))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()
    print('Load ALL')
    
