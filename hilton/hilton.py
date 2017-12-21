#!
import requests
from bs4 import BeautifulSoup
import urllib
from urllib.parse import parse_qs
import threading
import time

##############################
#ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
header = {'User-Agent':ua_mo}


#gh = Ghost()

#se = Session(gh, user_agent=ua, wait_timeout=20, wait_callback=None, display=True, viewport_size=(800, 680), download_images=True)

#se_mo = Session(gh, user_agent=ua_mo, wait_timeout=20, wait_callback=None, display=True, viewport_size=(375, 553), download_images=True)
###############################

city_list = ['Anshun', 'Aomen', 'beijing', 'benxi', 'changzhou', 'chongqing', 'dandong', 'dalian', 'fuzhou', 'foshan', 'guiyang', 'guangzhou', 'geermu', 'huizhou', 'hangzhou', 'hefei', 'haikou', 'jiaxing', 'jiuzhaigou', 'jilin', 'jinan', 'linzhi', 'lijiang', 'ningbo', 'putian', 'qingdao', 'quanzhou', 'sanqingshan', 'shiyan', 'suzhou', 'shanghai', 'shenzhen', 'suzhou', 'shengyang', 'shijiazhang', 'sanya', 'tianjin', 'urumqi', 'wuxi', 'wuhu', 'wencheng', 'wuhan', 'HongKong', 'xian', 'xishuangbanna', 'xianggelila', 'xiamen', 'yantai', 'yuxi', 'zhoushan', 'zhongshan', 'zhengzhou', 'zhuzhou']

arrivalDate = '2017-12-17'
departureDate = '2017-12-18'

#def  hilton_url(arrivalDate, departureDate, city, country='China'):

def get_ctghocn(city):
    globals()[city] = []
    url = 'http://www.hilton.com.cn/zh-cn/city/%s-hotels.html' % city
    html = requests.get(url, headers = header, allow_redirects=False).content
    hilton_soup = BeautifulSoup(html, "html.parser")
    source = hilton_soup.select('a.city-booking')
    for i in range(len(source)):
        href = source[i].get('href')
        #print(href)
        ctghocn_code = href[-7:-1]
        #print(ctghocn_code)
        ctyhocn.append(ctghocn_code)
        globals()[city].append(ctghocn_code)
    globals()[city] = list(set(globals()[city]))
    if city == 'guiyang':
        globals()['guiyang'] = ['KWEGUGI']
    ctyhocn_list[str(city)] = globals()[city]
    print(len(globals()[city]))

ctyhocn_list = {}
ctyhocn = []
threads = []
for i in city_list:
    a = threading.Thread(target=get_ctghocn, args=(i,))
    threads.append(a)
    a.start()

for t in threads:
    t.join()

ctyhocn = list(set(ctyhocn))
len(ctyhocn)
len(ctyhocn_list)

for i in list(ctyhocn_list):
    print("-------------%s-----------" % i)
    for l in ctyhocn_list[i]:
        print(l)


def get_price(code):
    globals()[code] = {}
    url = 'https://secure3.hilton.com/zh_CN/hi/reservation/book.htm?ctyhocn=%s&arrivalDate=%s&departureDate=%s&hhonorsRate=false&numberOfRooms=1&inputModule=HOTEL_SEARCH&internalDeepLinking=true&toAvailCalendar=true' % (code, arrivalDate, departureDate)
    #print(url)
    html = requests.get(url, headers = header).content
    hilton_soup = BeautifulSoup(html, "html.parser")
    hotel = hilton_soup.select('h1 > span')[0].text
    address = hilton_soup.select('span.adr')[0].text
    tel = hilton_soup.select('span.tel')[0].text
    print('---------------%s---------------' % hotel)
    print('------%s---' % address)
    for x in range(len(hilton_soup.select('tr.selectable'))):
        date = hilton_soup.select('tr.selectable')[x].select('strong')[0].text
        price = hilton_soup.select('tr.selectable')[x].select('strong')[2].text
        print(date, price)
        date = date.split()[0] + '-' + date.split()[2]
        globals()[code][date] = price
    print('--------------------end------------------')

# https://secure3.hilton.com/en_US/hi/reservation/book.htm?ctyhocn=SHAHITW&hhonorsRate=false&numberOfRooms=1&inputModule=HOTEL_SEARCH&internalDeepLinking=true&toAvailCalendar=true


def get_city(code):
    for i in ctyhocn_list.items():
        for l in i[1]:
            if l == code:
                city = i[0]
                index = i[1].index(l)
                return city, index










tt = requests.get('http://www.hilton.com.cn/zh-cn/city/linzhi-hotels.html', headers = header)
