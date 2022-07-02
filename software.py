# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 16:44
#@Author: TephrocactusHC
#@File: software.py
#@Project: NKUSpider
#@Software: PyCharm
'''

from bs4 import BeautifulSoup as bs
import requests
import re

root_url = 'https://cs.nankai.edu.cn/'
urls = ['https://cs.nankai.edu.cn/szll/jslb.htm', 'https://cs.nankai.edu.cn/szll/jslb/2.htm',
        'https://cs.nankai.edu.cn/szll/jslb/1.htm', 'https://cs.nankai.edu.cn/szll/tpyjy.htm']
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def find_teacher(url):
    url = url.replace('../', '')
    response = requests.get(root_url + url, headers=headers)
    response.encoding = 'utf-8'
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result


def find_teacher_list(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('#techerinformationList tbody tr td .span3.div-inline a')
    with open(r'D:\MYCODE\NKUSpider\software.txt', 'a', encoding='utf-8') as f:
        for teacher in teacher_list:
            name = teacher['title']
            email_list = find_teacher(teacher['href'])
            email_list = list(set(email_list))
            email_list.remove('MP-@J.GzNuj')
            print(name, email_list)
            f.write(f'软件学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)
