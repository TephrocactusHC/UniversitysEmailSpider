# -*- coding = 'utf-8' -*-
'''
#@Time: 2022/7/2 20:22
#@Author: TephrocactusHC
#@File: zhouenlai.py
#@Project: NKUSpider
#@Software: PyCharm
'''
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
root_url='https://zfxy.nankai.edu.cn/faculty/'

urls=['https://zfxy.nankai.edu.cn/faculty/political_science.htm',
     'https://zfxy.nankai.edu.cn/faculty/public_administration.htm',
     'https://zfxy.nankai.edu.cn/faculty/international_relations.htm',
     'https://zfxy.nankai.edu.cn/faculty/sociology.htm',
     'https://zfxy.nankai.edu.cn/faculty/socialwork.htm',
     'https://zfxy.nankai.edu.cn/faculty/psychology.htm',
     'https://zfxy.nankai.edu.cn/faculty/IHE.htm']

def find_teacher(url):
    browser.get(root_url + url)
    response = browser.page_source
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)|\（AT\）|#|[*]', '@', response, re.I)
    result = result.replace('(AT)', '@')
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result

for url in urls:
    browser.get(url)
    response = browser.page_source
    page = bs(response, 'html.parser')
    teacher_list = page.select('.teacherbox .teacherimgbox a')
    with open(r'D:\MYCODE\NKUSpider\zhouenlai.txt', 'a', encoding='utf-8') as f:
         for teacher in teacher_list:
             name = teacher.select('img')[0]['alt']
             email_list = find_teacher(teacher['href'])
             email_list = list(set(email_list))
             print(name, email_list)
             f.write(f'周恩来政府管理学院\t{name}')
             for email in email_list:
                  f.write(f'\t{email}')
             f.write('\n')
