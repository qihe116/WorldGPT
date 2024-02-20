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


def a_page1(pages):  # 同花顺全部股票一页20个股票行情
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

def a_pages():  # 同花顺全部股票所有页股票行情 需要休市时候运行 否则可能会出现重复缺失股票信息
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
    df.to_excel('tonghuashun.xlsx', index=False)

# a_pages()
df1 = pd.read_excel('tonghuashun.xlsx')
lis = df1.values.tolist()
codes = [k[1] for k in lis]
print(len(set(codes)))
print(len(codes))
```

tmp
