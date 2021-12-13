from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import re
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

try:
    for k in range(5, 21):
        url = 'https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseList.do?diseaseKindId=C00000{}'.format(k)
        driver.get(url)
        Disease = []
        Content = []
        for i in range(1, 9): #페이지수
            try:
                if i >= 2:
                    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/span/a[{}]'.format(i)).click()
            except:
                print(i, ' 페이지없음')
            for j in range(1, 21): #데이터수
                print(i, 'page', j, '번째 크롤링 중')
                try:
                    asan_title_xpath = '//*[@id="listForm"]/div/div/ul/li[{}]/div[2]/strong/a'.format(j)
                    title = driver.find_element_by_xpath(asan_title_xpath).text
                    print(title)
                    try:
                        driver.find_element_by_xpath(asan_title_xpath).click()
                        content = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]').text
                        #time.sleep(3)
                        # print(content)
                        Disease.append(title)
                        # print(len(Disease))
                        Content.append(content)
                        # print(len(Content))
                        driver.back()
                    except:
                        print('main text error')
                except:
                    print('error', '내용없음')
            print(len(Disease))
        df_content = pd.DataFrame({'Disease': Disease, 'Content': Content})
        df_content.to_csv('./crawling/disease_asan_{}.csv'.format(k), index=False)
        print(df_content)

except:
    print('totally error')