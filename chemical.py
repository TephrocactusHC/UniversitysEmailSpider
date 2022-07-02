# coding = utf-8
# @Time : 2022/6/30 14:41
# @Author : HC
# @File : chemical.py
# @Software : PyCharm

import re, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)


def get_main_pages():
    mainpages = []
    Departments = []
    browser.get("https://chem.nankai.edu.cn/hxx/main.htm")
    data = browser.page_source
    soup = bs(data, 'html.parser')
    source = soup.select('.nav2 ul ul li a')
    for i in source[0:6]:
        mainpages.append(i['href'])
        Departments.append(i.text)
    return mainpages, Departments


def get_thing(mainpages, Departments):
    rooturl = 'https://chem.nankai.edu.cn/_s312'
    root_url = 'https://chem.nankai.edu.cn'
    teacherlist = []
    for i in range(len(mainpages)):
        link = rooturl + mainpages[i]
        browser.get(link)
        data = browser.page_source
        soup = bs(data, 'html.parser')
        source = soup.select('.teacher-box div a')
        for j in source:
            link = root_url + j['href']
            browser.get(link)
            data1 = browser.page_source
            email = re.findall(r'邮件.*?>(.*?)</d', data1, re.S)
            p_email = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', email[0])
            if p_email != ['']:
                email = str(p_email).strip('[')
                email = email.strip(']')
                email = email.strip("'")
            else:
                email = ''
            teacher = Departments[i] + ',' + j.text + ',' + email + '\n'
            # print(teacher)
            teacherlist.append(teacher)
    return teacherlist


def writelist(teacherlist):
    with open(r'D:\NKUspider\chemical.txt', 'w', encoding='utf-8') as f:
        for teacher in teacherlist:
            f.write(teacher)


if __name__ == '__main__':
    mainpages, Departments = get_main_pages()
    teacherlist = get_thing(mainpages, Departments)
    writelist(teacherlist)
