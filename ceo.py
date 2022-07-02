# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 17:52
#@Author: TephrocactusHC
#@File: ceo.py
#@Project: NKUSpider
#@Software: PyCharm
'''

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re

urls = ['https://ceo.nankai.edu.cn/szll/xdgxyjs.htm', 'https://ceo.nankai.edu.cn/szll/gdzbmqjyjsyjs.htm',
        'https://ceo.nankai.edu.cn/szll/wdzgcx.htm', 'https://ceo.nankai.edu.cn/szll/dzkxygcx.htm',
        'https://ceo.nankai.edu.cn/szll/dzxxgcx.htm', 'https://ceo.nankai.edu.cn/szll/txgcx.htm',
        'https://ceo.nankai.edu.cn/szll/dzxxsyjxzx.htm']
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
root_url = 'https://ceo.nankai.edu.cn/szll/'


def find_teacher(url):
    response = requests.get(root_url + url, headers=headers)
    response.encoding = 'utf-8'
    result = re.findall('邮箱.*?<span class="marginRight56">\s*(.*?)\s*</span>', response.text, re.S)
    return result


for url in urls:
    thelist = []
    table = pd.read_html(url)[0]
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('tbody tr td a')
    for teacher in teacher_list:
        email_list = find_teacher(teacher['href'])
        email_list = list(set(email_list))
        thelist.append(email_list)
    table['邮箱'] = thelist
    print(table)
    if url == 'https://ceo.nankai.edu.cn/szll/xdgxyjs.htm':
        table.to_csv('ceo.csv', mode='a', index=False)
    else:
        table.to_csv('ceo.csv', mode='a', index=False, header=False)
