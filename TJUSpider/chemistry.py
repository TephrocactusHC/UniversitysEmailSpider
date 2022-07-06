from selenium import webdriver
import time, requests, re
from bs4 import BeautifulSoup as bs

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(options=chrome_options)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
root_url = 'http://chemeng.tju.edu.cn'
browser = webdriver.Chrome()
browser.maximize_window()
browser.get('http://chemeng.tju.edu.cn/cn/szdw')
cookies = browser.get_cookies()
data = browser.page_source
page = bs(data, 'html.parser')
teacher_list = page.select('.team ul li a')
browser.quit()
cookie_dict = {}
for item in cookies:
    cookie_dict[item['name']] = item['value']
print(cookie_dict)


def find_teacher(url):
    res = requests.get(root_url + url, headers=headers, cookies=cookie_dict)
    res.encoding = 'utf-8'
    result = re.sub('\[at\]|\(at\)| at |\(~at~\)', '@', res.text, re.I)
    result = re.sub('\[dot\]|\(dot\)| dot |\(~dot~\)|．', '.', result, re.I)
    result = re.findall('([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-\.]+)', result, re.S)
    if len(result) >= 4:
        return result[0:1]
    else:
        return result[:-1]


with open(r'D:\MYCODE\TJUSpider\chemistry.txt', 'a', encoding='utf-8') as f:
    for teacher in teacher_list:
        name = teacher.text
        email_list = find_teacher(teacher['href'])
        email_list = list(set(email_list))
        print(name, email_list)
        f.write(f'化工学院\t{name}')
        for email in email_list:
            f.write(f'\t{email}')
        f.write('\n')
