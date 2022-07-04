# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/4 14:22
#@Author: TephrocactusHC
#@File: lifescience.py
#@Project: NKUSpider
#@Software: PyCharm
'''

import re, requests, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
total_pages = []
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://sky.nankai.edu.cn/7798/list.htm')
time.sleep(5)

browser.find_element(By.CSS_SELECTOR, '#search_teach > li:nth-child(1) > a').click()
time.sleep(5)
data = browser.page_source
soup = bs(data, 'html.parser')
source = soup.select('.news-main.clearfix li a')
for i in source:
    total_pages.append(i['href'])

browser.find_element(By.CSS_SELECTOR, '#search_teach > li:nth-child(2) > a').click()
time.sleep(5)
data = browser.page_source
soup = bs(data, 'html.parser')
source = soup.select('.news-main.clearfix li a')
for i in source:
    total_pages.append(i['href'])

browser.find_element(By.CSS_SELECTOR, '#search_teach > li:nth-child(3) > a').click()
time.sleep(5)
data = browser.page_source
soup = bs(data, 'html.parser')
source = soup.select('.news-main.clearfix li a')
for i in source:
    total_pages.append(i['href'])

for page in total_pages:
    res = requests.get(page, headers=headers)
    res.encoding = 'utf-8'
    soup = bs(res.text, 'html.parser')
    name = soup.select('.navcon')[0]['tip']
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', res.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    email = re.findall('邮箱：  (.*?)</p>', result, re.S)
    email = list(set(email))[0]
    print(name, email)
    with open(r'D:\MYCODE\NKUSpider\lifescience.txt', 'a', encoding='utf-8') as f:
        f.write(f'生命科学学院\t{name}\t{email}\n')
