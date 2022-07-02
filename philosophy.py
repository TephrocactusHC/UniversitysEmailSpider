# coding = utf-8
# @Time : 2022/6/29 11:07
# @Author : HC
# @File : philosophy.py
# @Software : PyCharm

from bs4 import BeautifulSoup as bs
import requests
import re

urls = [
    'http://phil.nankai.edu.cn/2017/0630/c6722a70411/page.htm',
    'http://phil.nankai.edu.cn/2017/0630/c6722a70410/page.htm',
    'http://phil.nankai.edu.cn/2017/0630/c6722a70409/page.htm'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def find_teacher(url):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
        result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
        return result
    except Exception as e:
        return []


def find_teacher_list(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.wp_articlecontent a')
    with open('philosophy.txt', 'a') as f:
        for teacher in teacher_list:
            name = teacher.select_one('span')
            if name:
                name = name.get_text().strip()
            else:
                continue
            email_list = find_teacher(teacher['href'])
            email_list = list(set(email_list))
            print(name, email_list)
            f.write(f'哲学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)
