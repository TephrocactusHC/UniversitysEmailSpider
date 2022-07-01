#coding = utf-8
#@Time : 2022/7/1 23:05
#@Author : HC
#@File : pharmacy.py
#@Software : PyCharm

from bs4 import BeautifulSoup as bs
import requests
import re


root_url = 'https://pharmacy.nankai.edu.cn/szdw'
urls = [
    '/js.htm',
    '/fjs.htm',
    '/js1.htm',
]


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def find_teacher(url):
    response = requests.get('https://pharmacy.nankai.edu.cn/'+url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('body')
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', str(teacher_list), re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result


def find_teacher_list(url):
    response = requests.get(root_url+url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.content_Ul li a')
    with open(r'D:\NKUspider\pharmacy.txt', 'a', encoding = 'utf-8') as f:
        for teacher in teacher_list:
            name = teacher.text
            email_list = find_teacher(teacher['href'])[:-1]
            email_list = list(set(email_list))
            print(name, email_list)
            f.write(f'药学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)