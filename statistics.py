# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 19:56
#@Author: TephrocactusHC
#@File: statistics.py
#@Project: NKUSpider
#@Software: PyCharm
'''
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
urls = [
    'https://stat.nankai.edu.cn/8081/list.htm','https://stat.nankai.edu.cn/8081/list2.htm'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

for url in urls:
    browser.get(url)
    response = browser.page_source
    page = bs(response, 'html.parser')
    email_list = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', response, re.S)[:-1]
    name_list = page.select('[style="font-size:18px;font-weight:bold;margin-top:0px;"]')
    with open(r'D:\MYCODE\NKUSpider\statistics.txt', 'a', encoding='utf-8') as f:
        for i in range(len(name_list)):
            name,post,=name_list[i].text.split()
            email=email_list[i]
            print(name,post,email)
            f.write(f'统计与数据科学学院\t{name}\t{post}\t{email}\n')