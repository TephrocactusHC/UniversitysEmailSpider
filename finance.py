# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/4 15:40
#@Author: TephrocactusHC
#@File: finance.py
#@Project: NKUSpider
#@Software: PyCharm
'''

import re, requests, time
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
urls = ['https://finance.nankai.edu.cn/js_19772/list.htm',
        'https://finance.nankai.edu.cn/js_19772/list2.htm',
        'https://finance.nankai.edu.cn/fjs/list.htm',
        'https://finance.nankai.edu.cn/js_19775/list.htm',
        'https://finance.nankai.edu.cn/zrfjs/list.htm',
        'https://finance.nankai.edu.cn/zrfjs_24256/list.htm',
        'https://finance.nankai.edu.cn/zljs/list.htm']
total_table = pd.DataFrame()
for url in urls:
    table = pd.read_html(url)[0]
    table_new = pd.DataFrame(table.to_numpy().reshape(-1, 1))
    total_table = pd.concat([total_table, table_new])
total_table = total_table.dropna()
total_table.to_csv(r'D:\MYCODE\NKUSpider\finance.txt', index=False, header=0)
