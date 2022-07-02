#coding = utf-8
#@Time : 2022/7/1 10:13
#@Author : HC
#@File : history.py
#@Software : PyCharm

from bs4 import BeautifulSoup as bs
import requests
import re


urls = [
    'https://history.nankai.edu.cn/16054/list.htm',
    'https://history.nankai.edu.cn/16055/list.htm',
    'https://history.nankai.edu.cn/16056/list.htm'
]


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def find_teacher(url):
    response = requests.get('https://history.nankai.edu.cn'+url, headers=headers)
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result[:-1]


def find_teacher_list(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.wp_subcolumn_list li ul li')
    print(teacher_list)
    with open(r'D:\NKUspider\history.txt', 'a', encoding='utf-8') as f:
        for teacher in teacher_list:
            name = teacher.select_one('a div .teacher_list_content_p').text
            name = re.sub(' +|\▪|\t+|\n|\r', '', name, re.S)
            email_list = find_teacher(teacher.select_one('a')['href'])
            email_list = list(set(email_list))
            print(name, email_list)
            f.write(f'历史学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)