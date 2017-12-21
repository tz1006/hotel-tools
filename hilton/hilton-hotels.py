# ！
import requests
from bs4 import BeautifulSoup
import sqlite3
import threading
import datetime

def load_codes():
    global codes
    codes = []
    conn = sqlite3.connect('database/hilton.db')
    c = conn.cursor()
    code = c.execute("SELECT ID from HILTON;")
    for c in code:
        if c[0] != '未开业':
            codes.append(c[0])
    conn.commit()
    conn.close()

load_codes()

today = datetime.date.today()
arrivalDate = '%s-%s-%s' % (today.year, today.month, today.day)
departureDate = '%s-%s-%s' % (today.year, today.month, today.day+1)

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

def create_hotel(form):
    conn = sqlite3.connect('database/hilton.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS %s
        (NAME TEXT PRIMARY KEY UNIQUE,
        ID   TEXT  );''' % form)
    print("Table created successfully")
    conn.commit()
    conn.close()
    print("%s Created!" % form)

