#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: queue.py


import queue
from concurrent.futures import ThreadPoolExecutor, as_completed



from hyatt import *

class hyatt():
    def __init__(self):
        driver = webdriver(1000, 20)
        self.Start()
    def Download(self, date):
        inlist = self.inlist()
        if date not in inlist:
            self.Q.put(date)
    def inlist(self):
        li = os.listdir('data')
        result = []
        for i in li:
            date = i.split('.')[0]
            result.append(date)
        if type(self.downloading) == type(''):
            result.append(self.downloading)
        return result
    def Start(self):
        self.Q = queue.Queue()
        self.downloading = True
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(self.Downloader)
    def Downloader(self)
        while self.downloading != False:
            date = self.Q.get()
            if date != 0:
                download(date)
            else:
                print('exit!')
    def Exit(self):
        self.downloading == False
        self.Q.clear()
        self.Q.put(0)


