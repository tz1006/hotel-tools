#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: webdriver.py


from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])


class webdriver():
    def __init__(self, limit=15):
        self.create_driver()
        self.limit = limit
    def create_driver(self):
        self.driver = Chrome('./chromedriver', options=option)
        self.driver.set_window_size(800, 900)
        self.count = 0
    def delete_driver(self):
        self.driver.exit()
    def get_page(self, url):
        if self.count == self.limit:
            self.create_driver()
            print('重启浏览器')
        self.driver.get(url)
        self.count += 1
        html = self.driver.page_source
        return html
    
