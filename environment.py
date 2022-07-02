# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 12:50
#@Author: TephrocactusHC
#@File: environment.py
#@Project: NKUSpider
#@Software: PyCharm
'''

from bs4 import BeautifulSoup as bs
import requests
import re

root_url = 'https://env.nankai.edu.cn'
urls = [
    '/14180/list.htm',
    '/14181/list.htm',
    '/14182/list.htm',
    '/14183/list.htm'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def find_teacher(url):
    response = requests.get(root_url + url, headers=headers)
    response.encoding = 'utf-8'
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result[1:-2]


def find_teacher_list(url):
    response = requests.get(root_url + url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.albumn_info .Article_Title a')
    with open(r'D:\MYCODE\NKUSpider\environment.txt', 'a', encoding='utf-8') as f:
        for teacher in teacher_list:
            name = teacher.text
            email_list = list(set(find_teacher(teacher['href'])))
            print(name, email_list)
            f.write(f'环境科学与工程学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)
