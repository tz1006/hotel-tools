#!

import requests
from bs4 import BeautifulSoup
import yaml

def query(key):
    query_url = 'https://www.ihg.com/guestapi/v1/ihg/cn/zh/web/suggestions?country=cn&language=zh&brand=ihg&query=%s' % key
    query_str = requests.get(query_url, headers = header, allow_redirects=False).content.decode(encoding ='utf-8')
    query_dict = yaml.load(query_str)
    print('-----------Result Cities------------')
    hotels = []
    for i in range(0, query_dict['preFilterCount']):
        print(query_dict['filteredSuggestionList'][i]['label'])
        hotels.append(query_dict['filteredSuggestionList'][i]['label'])
    # return hotels



he = {
'Host': 'apis.ihg.com',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://www.ihg.com/hotels/us/en/find-hotels/hotel/list?qDest=Los%20Angeles,%20CA,%20United%20States&qCiMy=02018&qCiD=2&qCoMy=02018&qCoD=3&qAdlt=1&qChld=0&qRms=1&qRtP=6CBARC&qAkamaiCC=US&qSrt=sDD&qBrs=ic.ki.ul.in.cp.vn.hi.ex.cv.rs.cw.sb.&qAAR=6CBARC&srb_u=1',
'Content-Type': 'application/json; charset=utf-8',
'X-IHG-MWS-API-Token': '58ce5a89-485a-40c8-abf4-cb70dba4229b',
'IHG-Language': 'en-US',
'X-IHG-API-KEY': 'se9ym5iAzaW8pxfBjkmgbuGjJcr3Pj6Y',
'Content-Length': '346',
'Origin': 'https://www.ihg.com',
'Connection': 'keep-alive',
}

da = {
"version":"1.3",
"checkDailyPointsCost":"true",
"corporateId":"",
"stay":{
    "travelAgencyId":"",
    "dateRange":{
        "start":"2018-01-02",
        "end":"2018-01-03"
    },
    "rateCode":"6CBARC",
    "children":0,
    "adults":1,
    "rooms":1
},
"radius":50,
"bulkAvailability":"true",
"marketingRates":"",
"location":{
    "lng":-118.242798,
    "lat":34.0522,
    "location":"Los Angeles, CA
    , United States"
}
}
