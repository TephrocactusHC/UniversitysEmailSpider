# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 13:14
#@Author: TephrocactusHC
#@File: tourism.py
#@Project: NKUSpider
#@Software: PyCharm
'''

from bs4 import BeautifulSoup as bs
import requests
import re

root_url = 'https://tas.nankai.edu.cn/'
urls = [
    'szll/zzjs/lyxx.htm',
    'szll/zzjs/lyxx/2.htm',
    'szll/zzjs/lyxx/1.htm',
    'szll/zzjs/hzjjyglx.htm'
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
    return result


def find_teacher_list(url):
    response = requests.get(root_url + url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.project-List ul li a')
    with open(r'D:\MYCODE\NKUSpider\tourism.txt', 'a', encoding='utf-8') as f:
        for teacher in teacher_list:
            name = teacher.get_text()
            name = name.replace('\n', '')
            email_list = find_teacher(teacher['href'])
            email_list = list(set(email_list))
            print(name, email_list)
            f.write(f'旅游与服务学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)
