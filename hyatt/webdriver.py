#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: webdriver.py


from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
import string
import zipfile
 
def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """代理认证插件
 
    args:
        proxy_host (str): 你的代理地址或者域名（str类型）
        proxy_port (int): 代理端口号（int类型）
        proxy_username (str):用户名（字符串）
        proxy_password (str): 密码 （字符串）
    kwargs:
        scheme (str): 代理方式 默认http
        plugin_path (str): 扩展的绝对路径
 
    return str -> plugin_path
    """
    
 
    if plugin_path is None:
        plugin_path = 'vimm_chrome_proxyauth_plugin.zip'
 
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
 
    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };
 
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
 
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }
 
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
 
    return plugin_path



proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host = 'http-dyn.abuyun.com',
    proxy_port = 9020,
    proxy_username = 'H557HX96M9Y0G15D',
    proxy_password = '8370941EDCC9ED02'
)




option = ChromeOptions()
#option.add_argument("--proxy-server=http://202.20.16.82:10152")
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_extension(proxyauth_plugin_path)



class webdriver():
    def __init__(self, limit=15, timeout=30):
        self.limit = limit
        self.timeout = timeout
        self.create_driver()
    def create_driver(self):
        self.driver = Chrome('./chromedriver', options=option)
        self.driver.set_window_size(800, 900)
        self.driver.set_page_load_timeout(self.timeout)
        self.count = 0
    def delete_driver(self):
        self.driver.quit()
        self.create_driver()
        print('重启浏览器')
    def get_page(self, url):
        load_count = 0
        while load_count <= 3:
            load_count += 1
            try:
                self.driver.get(url)
                break
            except:
                if load_count == 4:
                    html = False
                    return html
        #WebDriverWait(self.driver, 1).until(EC.url_changes(url))
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
            html = self.driver.page_source
        except:
            html = None
        self.count += 1
        if self.count == self.limit:
            self.delete_driver()
            time.sleep(2)
        return html


if __name__ == '__main__':
    driver = webdriver(1000, 20)
    import code
    code.interact(banner="", local=locals())

#driver.delete_driver()
#dd = driver.get_page(ip)
# https://www.hyatt.com/zh-CN/shop/rates/guihr?rooms=1&adults=1&checkinDate=2019-05-16&checkoutDate=2019-05-19&kids=0&offercode=CUP19&rateFilter=standard
