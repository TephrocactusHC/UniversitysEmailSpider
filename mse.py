# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 15:23
#@Author: TephrocactusHC
#@File: mse.py
#@Project: NKUSpider
#@Software: PyCharm
'''

from bs4 import BeautifulSoup as bs
import requests, re

root_url = 'https://mse.nankai.edu.cn'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def find_teacher(url):
    if url.startswith('h'):
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
        result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    else:
        response = requests.get(root_url + url, headers=headers)
        response.encoding = 'utf-8'
        email = re.findall('电子邮箱 ：(.*?)</li>', response.text, re.S)
        result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', str(email), re.I)
        result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result


def find_teacher_list():
    response = requests.get('https://mse.nankai.edu.cn/9281/list.htm', headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.wp_subcolumn_list li ul li span a')
    with open(r'D:\MYCODE\NKUSpider\mse.txt', 'a', encoding='utf-8') as f:
        for teacher in teacher_list:
            name = teacher.get_text()
            email_list = find_teacher(teacher['href'])
            email_list = list(set(email_list))
            print(name, email_list)
            f.write(f'材料科学与工程学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


find_teacher_list()
