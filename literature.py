# coding = utf-8
# @Time : 2022/7/1 23:40
# @Author : HC
# @File : literature.py
# @Software : PyCharm


from bs4 import BeautifulSoup as bs
import requests
import re

urls = ['https://wxy.nankai.edu.cn/zgyywxx/list.htm',
        'https://wxy.nankai.edu.cn/dfysx/list.htm',
        'https://wxy.nankai.edu.cn/yssjx/list.htm',
        'https://wxy.nankai.edu.cn/whszjxb/list.htm']

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
        result = re.findall('>(.*?)<', result, re.S)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', str(result))
    except requests.exceptions.MissingSchema as e:
        response = requests.get('http://wxy.nankai.edu.cn' + url, headers=headers)
        response.encoding = 'utf-8'
        result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
        result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
        result = re.findall('>(.*?)<', result, re.S)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', str(result))
    return result


def find_teacher_list(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('div.albumn_info .Article_Title a')
    with open(r'D:\NKUspider\literature.txt', 'a', encoding='utf-8') as f:
        for teacher in teacher_list:
            name = teacher.text
            email_list = find_teacher(teacher['href'])[:-1]
            email_list = list(set(email_list))
            print(name, email_list)
            f.write(f'文学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


for url in urls:
    find_teacher_list(url)
