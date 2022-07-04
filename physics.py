# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/4 10:42
#@Author: TephrocactusHC
#@File: physics.py
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
# browser = webdriver.Chrome()
browser.get('https://physics.nankai.edu.cn/3193/list.htm')
time.sleep(3)
data_all = browser.page_source
for i in range(11):
    browser.find_element(By.CSS_SELECTOR, '#wp_paging_w6 > div > ul > li.new_page_nav > a.next').click()
    time.sleep(3)
    data = browser.page_source
    data_all += data
soup = bs(data_all, 'html.parser')
source = soup.select('.news-main.clearfix li a')
for i in source:
    total_pages.append(i['href'])
# print(total_pages)

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
    with open(r'D:\MYCODE\NKUSpider\physics.txt', 'a', encoding='utf-8') as f:
        f.write(f'物理学院\t{name}\t{email}\n')
