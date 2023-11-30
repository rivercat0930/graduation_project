import requests
from bs4 import BeautifulSoup

import os
import re
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import json
import emoji

from time import sleep

print(re.sub("^:[.]+:$", ":rolling_on_the_floor_laughing:", ""))

### 從表中抓地名
title_list = []
f_title_list = open("./src/main/resources/location.txt", "r").readlines()
for title in f_title_list:
    title_list.append(title.replace("\n", ""))


for title_name in title_list:
    f_review = []
    browser = webdriver.Chrome()
    browser.get("https://www.google.com/maps/")
    # browser.get('https://goo.gl/maps/73AVr7DgQeDzh3yj9')

    # 定位搜尋框
    element = browser.find_element(By.ID, "searchboxinput")

    # 傳入字串
    element.send_keys(title_name)

    button = browser.find_element(By.CLASS_NAME, "mL3xi")
    button.click()
    time.sleep(3)

    try:
        button1 = browser.find_elements(By.CLASS_NAME, "M77dve")
        for k in button1:
            if "更多評論" in k.text:
                k.click()
                time.sleep(3)
                break
    except Exception as e:
        print(title_name)

    # soup = Soup(browser.page_source,"lxml")
    # all_reviews = soup.find_all(class_ = 'wiI7pd')
    # print(all_reviews)
    soup = Soup(browser.page_source, "lxml")

    EX = r":[a-zA-Z0-9_.+-]+:"
    # 評論分頁下滑
    for i in range(30):
        try:
            pane = browser.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf")
            browser.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", pane
            )
            time.sleep(3)
            # soup = Soup(browser.page_source, "lxml")
            # all_reviews = soup.find_all(class_='wiI7pd')
        # print(all_reviews)
        except Exception as e:
            print(title_name)
            print(e)
            all_reviews = []

    all_reviews = browser.find_elements(By.CLASS_NAME, "wiI7pd")

    for j in all_reviews:
        try:
            button2 = browser.find_elements(By.CLASS_NAME, "w8nwRe.kyuRq")
            for k in button2:
                if "全文" in k.text:
                    k.click()
                    time.sleep(3)
                    break
        except Exception as e:
            print(title_name)
            print(e)

        s = j.text.replace("\n", ",")
        # content =re.sub('^:[.]+:$',emoji.demojize(s),'')
        content = emoji.demojize(s)
        content = re.sub(EX, "", content)
        # print(re.sub(EX, '', content))
        f_review.append(content)

    print(f_review)
    with open(
        f"./src/main/resources/location_comment/{title_name}comment.txt",
        "w",
        encoding="utf-8",
    ) as f:
        # json.dump(f_review, indent=4, fp=f, ensure_ascii=False)
        for line in f_review:
            f.write(line)
            f.write("\n")
        print(f"../src/main/resources/location_comment/{title_name}comment.txt")

    browser.close()
# output_data = json.dump(f_review, indent = 4)


# all_reviews = soup.find_all('span')
# print(all_reviews)
"""
# 點擊返回店家頁面
WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'geoUxComponentsAppbarButtonWrapper')))
BacktoStore_btn = browser.find_element(By.CLASS_NAME,'geoUxComponentsAppbarButtonWrapper')[0]
BacktoStore_btn.click()

# 點擊返回搜尋結果
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-back-to-list-button.blue-link.noprint')))
back_btn = browser.find_element(By.CLASS_NAME,'section-back-to-list-button.blue-link.noprint')[0]
back_btn.click()

"""
###抓文章標題網址用

# taichung = "https://www.taiwan.net.tw/"
# data_urls = []
# print("get url...")
# title_write = open("titles.txt", "a", encoding="utf-8")
# for i in range(1,16):
#     url = "https://www.taiwan.net.tw/m1.aspx?sNo=0000064&keyString=%5e3%5e%5e&page="+str(i)
#     response = requests.get(url)
#     sleep(0.1)
#     soup = BeautifulSoup(response.text, "html.parser")
#     #titles = soup.find_all("div", class_="card-title")
#     titles_url = soup.find_all("a", class_="card-link")
#     for i in titles_url:
#         # print(i['title']+','+i['href'])
#         # data_urls.append(taichung+i['href'])
#         title_write.writelines(f'{i["title"]}')
#         title_write.writelines(f'\n')
#         print(i['title'])
# print("Finish")
###抓文章標題網址用###
