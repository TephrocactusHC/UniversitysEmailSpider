# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 18:53
#@Author: TephrocactusHC
#@File: AI.py
#@Project: NKUSpider
#@Software: PyCharm
'''

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
urls = ['https://ai.nankai.edu.cn/szdw/js_yjy_.htm', 'https://ai.nankai.edu.cn/szdw/fjs_fyjy_.htm',
        'https://ai.nankai.edu.cn/szdw/j_s.htm', 'https://ai.nankai.edu.cn/szdw/syjxdw.htm',
        'https://ai.nankai.edu.cn/szdw/bsh.htm']
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
root_url = 'https://ai.nankai.edu.cn/'

def find_teacher(url):
    url=url.replace('../', '')
    browser.get(root_url + url)
    response = browser.page_source
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result, re.S)
    return result


for url in urls:
    thelist = []
    table = pd.read_html(url)[1]
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.am-table.am-table-bordered.am-table-striped.am-table-centered.am-table-hover.gage-table tbody tr td a')
    for teacher in teacher_list:
        email_list = find_teacher(teacher['href'])
        email_list = list(set(email_list))
        thelist.append(email_list)
    table['邮箱'] = thelist
    # print(thelist)
    if url == 'https://ai.nankai.edu.cn/szdw/js_yjy_.htm':
        table.to_csv('AI.csv', index=False)
    else:
        table.to_csv('AI.csv', mode='a', index=False, header=False)
