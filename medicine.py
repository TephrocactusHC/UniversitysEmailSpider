# coding = utf-8
# @Time : 2022/7/1 14:25
# @Author : HC
# @File : medicine.py
# @Software : PyCharm


import re, requests
from bs4 import BeautifulSoup as bs

urls = ['https://medical.nankai.edu.cn/6612/list.htm',
        'https://medical.nankai.edu.cn/6613/list.htm',
        'https://medical.nankai.edu.cn/6614/list.htm',
        'https://medical.nankai.edu.cn/6615/list.htm',
        'https://medical.nankai.edu.cn/6616/list.htm',
        'https://medical.nankai.edu.cn/6617/list.htm',
        'https://medical.nankai.edu.cn/6619/list.htm',
        'https://medical.nankai.edu.cn/6620/list.htm',
        'https://medical.nankai.edu.cn/6621/list.htm',
        'https://medical.nankai.edu.cn/6622/list.htm',
        'https://medical.nankai.edu.cn/6623/list.htm',
        'https://medical.nankai.edu.cn/dszxyybssds/list.htm',
        'https://medical.nankai.edu.cn/tjszxfckyy/list.htm',
        'https://medical.nankai.edu.cn/tjsykyy/list.htm'
        # 'https://medical.nankai.edu.cn/tjsdermyy/list.htm'
        ]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

root_url = 'https://medical.nankai.edu.cn/'


def find_teacher(url):
    response = requests.get(root_url + url, headers=headers)
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', response.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result)
    return result


def find_teacher_list(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    page = bs(response.text, 'html.parser')
    teacher_list = page.select('.teacher-list .item a')
    with open(r'D:\NKUspider\medicine.txt', 'a', encoding='utf-8') as f:
        for teacher in teacher_list:
            name = teacher.get_text()
            name = re.sub(' +|\t+|\n|\r', '', name, re.S)
            email_list = find_teacher(teacher['href'])
            email_list = list(set(email_list))
            # print(name, email_list)
            f.write(f'医学院\t{name}')
            for email in email_list:
                f.write(f'\t{email}')
            f.write('\n')


def a_special():
    response = requests.get('https://medical.nankai.edu.cn/tjsdermyy/list.htm', headers=headers)
    response.encoding = 'utf-8'
    res = response.text
    with open(r'D:\NKUspider\medicine.txt', 'a', encoding='utf-8') as f:
        p_name = '<p>姓名：(.*?)</p>'
        name = re.findall(p_name, res, re.S)
        name = name[0]
        email = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', res, re.I)
        email = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', email, re.I)
        email = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', email)
        # print(name, email)
        f.write(f'医学院\t{name}')
        f.write(f'\t{email}')
        f.write('\n')


if __name__ == '__main__':
    for url in urls:
        find_teacher_list(url)

    a_special()
