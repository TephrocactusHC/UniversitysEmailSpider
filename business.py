# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 13:32
#@Author: TephrocactusHC
#@File: business.py
#@Project: NKUSpider
#@Software: PyCharm
'''
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

root_url = 'https://bs.nankai.edu.cn'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def get_secondary_pages():
    pagelist = []
    res = requests.get('https://bs.nankai.edu.cn/jstd/list.htm', headers=headers, timeout=10)
    res.encoding = 'utf-8'
    page = bs(res.text, 'html.parser')
    major_list = page.select('.szdw-zylist div div a')
    for major in major_list:
        pagelist.append(root_url + major['href'])
    return pagelist


def find_email(url):
    if url.startswith('h'):
        browser.get(url)
        res = browser.page_source
        result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', res, re.I)
        result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    else:
        browser.get(root_url + url)
        res = browser.page_source
        result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', res, re.I)
        result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result


def get_teacher_list():
    pagelist = get_secondary_pages()
    for major in pagelist:
        res = requests.get(major, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        page = bs(res.text, 'html.parser')
        teachers = page.select('.szdw-newslist div a')
        with open(r'D:\MYCODE\NKUSpider\business.txt', 'a', encoding='utf-8') as f:
            for teacher in teachers:
                name = teacher.select('.con .t')[0].text.split()[0]
                teacher_page = teacher['href']
                email_list = list(set(find_email(teacher_page)))
                print(name, email_list)
                f.write(f'商学院\t{name}')
                for email in email_list:
                    f.write(f'\t{email}')
                f.write('\n')


if __name__ == '__main__':
    get_teacher_list()
