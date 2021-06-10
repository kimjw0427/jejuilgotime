# coding=<utf-8>
import requests
from bs4 import BeautifulSoup

time_range = ['08:10~09:00','09:10~10:00','10:10~11:00','11:10~12:00 ','11:10~12:00','13:00~13:50','14:00~14:50','15:00~15:50']
classroom = 2

url = 'https://jeil.jje.hs.kr/jeil-h/0208/board/16996'
url_content = url + '#contents'
html = BeautifulSoup(requests.get(url_content).text,'html.parser')
title = html.select_one('table.wb').select('tbody > tr > td > a')

dict = {}

num = 1
mon = 0
mon_ = 0

for i in title:
    url_code = str(i).split('"')[3].split("'")[3]
    url_title = str(i.text).replace('\n','').replace('\xa0','')
    temp_mon = int(url_title[0:2].replace('월',''))
    if temp_mon > mon_:
        if len(str(temp_mon)) == 2:
            mon_ = temp_mon
            mon = str(temp_mon)
        else:
            mon_ = temp_mon
            mon = '0'+str(temp_mon)
    dict[num] = url_code
    print(f'{num}. {url_title}')
    num += 1

print('\n======================================================\n')

def crawling(url_num):
    time_url = url +'/'+ str(url_num)
    time_html = BeautifulSoup(requests.get(time_url).text, 'html.parser')
    image_url = time_html.select_one('.fieldBox').select('dl > dd')
    image_url = 'http://jeil.jje.hs.kr/'+str(image_url).split('"')[9]
    image_num = requests.get(image_url).url.split('=')[1]
    doc_url = f'https://jeil.jje.hs.kr/upload/mobileBoard/2021{mon}/{image_num}.files/1.xhtml'
    print(doc_url)
    doc_html = BeautifulSoup(requests.get(doc_url).text, 'html.parser')
    doc_html = doc_html.select('span')
    for cl in range(len(doc_html)):
        for tr in time_range:
            if doc_html[cl].text == tr:
                if '영어' in doc_html[cl+classroom-1].text:
                    print(f'{tr.replace(" ","")} {doc_html[cl + classroom-1].text}\n')
                else:
                    print(f'{tr.replace(" ","")} {doc_html[cl + classroom].text}\n')

while(True):
    date = int(input('번호 / 0 = Exit: '))
    if date == '0':
        break
    elif date > len(dict) or date < 0:
        print('\n잘못된 번호입니다.\n')
    else:
        crawling(dict[date])
print('\n끝\n')
