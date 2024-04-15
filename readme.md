### WorldGPT
tmp

```python
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from tqdm import tqdm
import os
import random
import json
import akshare as ak


def ths_data_index():
    url = "https://q.10jqka.com.cn/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, timeout=2)
    content = response.read()
    html = BeautifulSoup(content, 'lxml')
    print(html)

def check_duplicate(df):
    lis = df.values.tolist()
    codes = [k[1] for k in lis]
    len1 = len(set(codes))
    len2 = len(codes)
    print(len1, len2)
    if len1 == len2:
        return 'no duplicate missing data'
    else:
        return 'error,there are duplicate missing data'

def a_page1(pages):  # 同花顺全部a股股票一页20个股票行情
    url = f"https://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{pages}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, timeout=2)
    content = response.read()
    html = BeautifulSoup(content, 'lxml')
    # print(html)
    div = html.find_all('table', class_='m-table m-pager-table')
    tbody = div[0].find_all('tbody')
    trs = tbody[0].find_all('tr')
    a20 = []
    for i in trs:
        td = i.find_all('td')
        res = [x.text for x in td]
        a20.append(res[:-1])
    return a20

def a_pages():  # 同花顺全部a股股票所有页股票行情 需要休市时候运行 否则可能会出现重复缺失股票信息
    a_s = []
    none_time = 0
    for i in tqdm(range(1, 300)):
        a20 = a_page1(str(i))
        if not a20:
            none_time += 1
        if none_time > 5:
            break
        a_s.extend(a20)
    df = pd.DataFrame(a_s, columns=['序号','代码','名称','现价','涨跌幅(%)','涨跌','涨速(%)','换手(%)','量比','振幅(%)','成交额','流通股','流通市值','市盈率'])
    print(check_duplicate(df))
    df.to_excel('tonghuashun.xlsx', index=False)
# a_pages()
def hk_page1(pages):  # 同花顺全部股票一页20个股票行情
    url = f"https://q.10jqka.com.cn/hk/detailYs/board/all/field/zdf/order/desc/page/{pages}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, timeout=2)
    content = response.read()
    html = BeautifulSoup(content, 'lxml')
    # print(html)
    div = html.find_all('table', class_='m-table m-pager-table')
    tbody = div[0].find_all('tbody')
    trs = tbody[0].find_all('tr')
    a20 = []
    for i in trs:
        td = i.find_all('td')
        res = [x.text for x in td]
        a20.append(res[:-1])
    # print(a20)
    return a20

def hk_pages():  # 同花顺全部股票所有页股票行情 需要休市时候运行 否则可能会出现重复缺失股票信息
    a_s = []
    none_time = 0
    for i in tqdm(range(1, 300)):
        a20 = hk_page1(str(i))
        if not a20:
            none_time += 1
        if none_time > 5:
            break
        a_s.extend(a20)
    df = pd.DataFrame(a_s, columns=["序号","代码","名称","现价","涨跌幅(%)","涨跌","换手(%)","成交量","市盈率","昨收","开盘价","最高价","最低价"])
    print(check_duplicate(df))
    df.to_excel('tonghuashun-hk.xlsx', index=False)
# hk_pages()
def usa_page1(pages):  # 美股
    url = f'https://q.10jqka.com.cn/usa/detailDefer/board/all/field/zdf/order/desc/page/{pages}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, timeout=2)
    content = response.read()
    html = BeautifulSoup(content, 'lxml')
    # print(html)
    div = html.find_all('table', class_='m-table m-pager-table')
    tbody = div[0].find_all('tbody')
    trs = tbody[0].find_all('tr')
    a20 = []
    for i in trs:
        td = i.find_all('td')
        res = [x.text for x in td]
        a20.append(res[:-1])
    # print(a20)
    return a20

def usa_pages():  # 美股 需要休市时候运行 否则可能会出现重复缺失股票信息
    a_s = []
    none_time = 0
    for i in tqdm(range(1, 300)):
        a20 = usa_page1(str(i))
        if not a20:
            none_time += 1
        if none_time > 5:
            break
        a_s.extend(a20)
    df = pd.DataFrame(a_s, columns=["序号","代码","名称","现价","涨跌幅(%)","涨跌","换手(%)","成交量","市盈率(%)","成交额","52周最高","52周最低"])
    print(check_duplicate(df))
    df.to_excel('tonghuashun-us.xlsx', index=False)
# usa_pages()
def usa_ch_page1(pages):  # 美股 中概股
    url = f'https://q.10jqka.com.cn/usa/detailDefer/board/zgg/field/zdf/order/desc/page/{pages}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, timeout=2)
    content = response.read()
    html = BeautifulSoup(content, 'lxml')
    # print(html)
    div = html.find_all('table', class_='m-table m-pager-table')
    tbody = div[0].find_all('tbody')
    trs = tbody[0].find_all('tr')
    a20 = []
    for i in trs:
        td = i.find_all('td')
        res = [x.text for x in td]
        a20.append(res[:-1])
    # print(a20)
    return a20

def usa_ch_pages():  # 美股 中概股 需要休市时候运行 否则可能会出现重复缺失股票信息
    a_s = []
    none_time = 0
    for i in tqdm(range(1, 300)):
        a20 = usa_ch_page1(str(i))
        if not a20:
            none_time += 1
        if none_time > 5:
            break
        a_s.extend(a20)
    df = pd.DataFrame(a_s, columns=["序号","代码","名称","现价","涨跌幅(%)","涨跌","换手(%)","成交量","市盈率(%)","成交额","52周最高","52周最低","所属板块","上市地"])
    print(check_duplicate(df))
    df.to_excel('tonghuashun-us-zgg.xlsx', index=False)
# usa_ch_pages()

# def a_info(stock_id):
#     # url = f'https://stockpage.10jqka.com.cn/{str(stock_id)}/company/#detail'
#     url = 'https://stockpage.10jqka.com.cn/000002/company/'
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
#     req = urllib.request.Request(url=url, headers=headers)
#     response = urllib.request.urlopen(req, timeout=2)
#     content = response.read()
#     html = BeautifulSoup(content, 'lxml')
#     print(html)
#     with open('test.html', 'w', encoding='utf8') as f:
#         f.write(html.decode())
#     div = html.find_all('div', class_='m_box company_overview company_detail')
#     print(len(div))
#     print(div)
# a_info(839946)

def hk_info(id_):
    url = f'https://basic.10jqka.com.cn/{id_}/company.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, timeout=2)
    content = response.read()
    html = BeautifulSoup(content, 'lxml')
    tbody = html.find_all('tbody')
    tds = tbody[0].find_all('td')
    res = {}
    for i in tds:
        pattern = re.compile(r'(.*\s*.*\s*)[：:](\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*.*\s*)')
        # pattern = re.compile(r'(.*)[：:](.*)', flags=re.DOTALL)
        key_value = pattern.findall(i.text)
        # print(key_value)
        key_, value_ = key_value[0]
        print(key_.strip(), value_.strip())
        res[key_.strip()] = value_.strip()
        # break
hk_info('HK2068')


# pattern = re.compile(r'(\S*)[：:](\s*\S*)')
# print(pattern.findall('主营业务： 工程勘察、设计及咨询、工程及施工承包、装备制造及贸易。'))

#240415
import urllib.request
proxy_handler = urllib.request.ProxyHandler({'http': 'http://127.0.0.1:8000'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
response = urllib.request.urlopen('http://httpbin.org/ip')
print(response.read().decode())

import requests
proxies = {
    "http": "http://127.0.0.1:8000",
    "https": "http://127.0.0.1:8000",}
response = requests.get('http://httpbin.org/ip',proxies=proxies)
print(response.content.decode())



```

tmp
