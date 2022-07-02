# coding = utf-8
# @Time : 2022/6/28 21:19
# @Author : HC
# @File : Marxism.py
# @Software : PyCharm

'''注意，不能频繁运行此程序，因为没有对第一个函数进行time.sleep的处理'''
'''本地文件推荐使用pandas读取，分隔符设为制表符\t'''
'''因为方便，就把名字、职位、院系、研究方向、邮箱都爬出来了'''

from bs4 import BeautifulSoup
from selenium import webdriver
import time, requests, re


def get_teachers_pages():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get("https://cz.nankai.edu.cn/13500/list.htm")
    time.sleep(5)
    data = browser.page_source
    soup = BeautifulSoup(data, 'html.parser')
    source = soup.select('body div div div div div div ul div div ul li a')

    TeacherList = []
    for i in source:
        TeacherList.append(i['href'])

    return TeacherList


def get_names_and_emails(TeacherPageList):
    ResultList = []
    for TeacherPage in TeacherPageList:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        url = TeacherPage
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        res = res.text

        p_name = '<h1 class="news_title">(.*?)</h1>'
        name = re.findall(p_name, res, re.S)
        teachername = name[0]

        p_post = '<p class="news_text"> 职称：  (.*?)</p>'
        post = re.findall(p_post, res, re.S)

        p_faculties = '<p class="news_text"> 院系：  (.*?)</p>'
        faculties = re.findall(p_faculties, res, re.S)

        p_major = '<p class="news_text"> 研究方向： (.*?)</p>'
        major = re.findall(p_major, res, re.S)

        p_email = '<p class="news_text"> Email：  (.*?)</p>'
        email = re.findall(p_email, res, re.S)

        result = teachername + '\t' + str(post[0]) + '\t' + str(faculties[0]) + '\t' + str(major[0]) + '\t' + str(
            email[0]) + '\n'
        result = re.sub('\r\n', '', result)
        result = re.sub('	&quot', '', result)
        ResultList.append(result)

    return ResultList


def write_results(ResultList):
    with open(r'D:\Marxism.txt', 'w') as f:
        f.write('姓名' + '\t' + '职位' + '\t' + '院系' + '\t' + '研究方向' + '\t' + '邮箱' + '\n')
        for result in ResultList:
            f.write(result)
    print('Finish!')


if __name__ == '__main__':
    TeacherPageList = get_teachers_pages()
    NaEList = get_names_and_emails(TeacherPageList)
    # print(NaEList)
    write_results(NaEList)
