# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 15:53
#@Author: TephrocactusHC
#@File: economy.py
#@Project: NKUSpider
#@Software: PyCharm
'''
from bs4 import BeautifulSoup as bs
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
myurl = 'https://economics.nankai.edu.cn/qzjs/list'
root_url = 'https://economics.nankai.edu.cn'


def find_email(url):
    response = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result[:-2]


for i in range(1, 11, 1):
    url = myurl + str(i) + '.htm'
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    page = bs(res.text, 'html.parser')
    teachers = page.select('[frag="窗口5"] div div p a')
    with open(r'D:\MYCODE\NKUSpider\economy.txt', 'a', encoding='utf-8') as f:
        for teacher in teachers:
            name = teacher.text
            teacher_page = root_url + teacher['href']
            email_list = list(set(find_email(teacher_page)))
            print(name, email_list)
            f.write(f'经济学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')
