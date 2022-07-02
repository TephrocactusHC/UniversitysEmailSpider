# coding = utf-8
# @Time : 2022/6/29 16:00
# @Author : HC
# @File : cs.py
# @Software : PyCharm


import re, requests, time
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver


def get_pages(url):
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = 'utf-8'
    res = res.text

    p_page = '<a style="color: #00A4E4" href="(.*?)">.*?</a>'
    pages = re.findall(p_page, res)
    table = pd.read_html(res)[0]

    return pages, table


def get_mytarget(pages):
    rooturl = 'https://cc.nankai.edu.cn/'
    emaillist = []
    for page in pages:
        link = rooturl + page
        res = requests.get(link, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        res = res.text
        p_email = '电子邮件：(.*?)</p>'
        email = re.findall(p_email, res, re.S)
        result = re.sub('\[at\]|\(at\)|at|\(~at~\)|#|\[AT\]|\(a\)', '@', email[0], re.I)
        result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
        result = re.sub('<.*?>', '', result)
        result = re.sub(' ', '', result)
        result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
        emaillist.append(result)
    return emaillist


def concat_email(emaillist, table):
    table['邮箱'] = emaillist
    return table


def main(urls):
    totaltable = pd.DataFrame()
    for url in urls:
        pages, table = get_pages(url)
        emaillist = get_mytarget(pages)
        table = concat_email(emaillist, table)
        totaltable = pd.concat([totaltable, table])
    totaltable.to_csv(r'D:\NKUspider\cs.csv', index=False)


if __name__ == '__main__':
    urls = [r'https://cc.nankai.edu.cn/jswyjy/list.htm#',
            'https://cc.nankai.edu.cn/fjswfyjy/list.htm',
            'https://cc.nankai.edu.cn/js/list.htm',
            'https://cc.nankai.edu.cn/syjxdw/list.htm'
            ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    main(urls)
