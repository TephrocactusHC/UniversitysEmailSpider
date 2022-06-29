#coding = utf-8
#@Time : 2022/6/29 14:34
#@Author : HC
#@File : fcollege.py
#@Software : PyCharm

import re,requests,time
from bs4 import BeautifulSoup as bs
from selenium import webdriver

def get_pages():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    url='https://fcollege.nankai.edu.cn/7189/list.htm'
    res=requests.get(url,headers=headers,timeout=10)
    res.encoding='utf-8'
    res=res.text

    p_page='<li class="sub-item i3.*?href="(.*?)" target="_self">(.*?)</a></li>'

    pages=re.findall(p_page,res)
    return pages

def spider(pages):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)
    root_url = 'https://fcollege.nankai.edu.cn/'

    resultList = []

    for eachpage in pages:
        page = root_url+eachpage[0]
        browser.get(page)
        time.sleep(5)
        data = browser.page_source
        soup = bs(data, 'html.parser')
        source = soup.select('body div div div div div div div div div ul li a')

        p_name = '<p class="tctlt t2" style="padding-top:6px;">(.*?)</p>'
        p_post = '<p>职称：(.*?)</p>'
        p_major = '<p>研究方向：(.*?)</p>'
        p_email = '<p>Email：(.*?)</p>'

        for i in source:
            i = str(i)
            name = re.findall(p_name, i)
            post = re.findall(p_post, i)
            major = re.findall(p_major, i)
            email = re.findall(p_email, i)
            result = eachpage[1] + '\t'+name[0] + '\t' + post[0] + '\t' + major[0] + '\t' + email[0] + '\n'
            print(result)
            resultList.append(result)

    return resultList

def write(resultList):
    with open(r'D:\fcollege.txt','w', encoding='utf_8') as f:
        for teacher in resultList:
            f.write(str(teacher))
    print('Finish!')

if __name__=='__main__':
    pages=get_pages()
    resultList=spider(pages)
    write(resultList)

