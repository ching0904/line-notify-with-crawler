from bs4 import BeautifulSoup
import requests
from requests import get
from datetime import datetime
import os

NOTIFY_TOKEN = os.environ['NOTIFY_TOKEN']
url = 'https://www.ptt.cc/'
web = requests.get('https://www.ptt.cc/bbs/Lifeismoney/index.html')
web.encoding='utf-8'       # 避免中文亂碼
soup = BeautifulSoup(web.text, "html.parser")
titles = soup.find_all('div', class_='title')
output = ''           # 建立 output 變數
for i in titles:
    if i.find('a') is not None:
        title_text = i.find('a').get_text()
        link = url + i.find('a')['href']
        if ('line' in title_text.lower() and 'point' in title_text.lower()) or 'lp' in title_text.lower():  # 搜索標題中包含 "line" 或 "lp" 的文章 不分大小寫
            output += title_text + '\n' + link + '\n\n'
        
if output != '':  
    headers = {
        "Authorization": "Bearer " + NOTIFY_TOKEN,
        "Content-Type": "application/x-www-form-urlencoded"
    }
 
    params = {"message": "\n" + output}
 
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  #200
else:
    headers = {
        "Authorization": "Bearer " + NOTIFY_TOKEN,
        "Content-Type": "application/x-www-form-urlencoded"
    }
 
    params = {"message": "沒有相關文章"}
 
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  #200表示沒有發生問題
