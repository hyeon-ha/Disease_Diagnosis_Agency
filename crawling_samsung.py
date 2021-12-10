# 카테고리
# //*[@id="tab-panel-search-type01"]/div/div/ul/li[1]/a
# //*[@id="tab-panel-search-type01"]/div/div/ul/li[2]/a
# //*[@id="tab-panel-search-type01"]/div/div/ul/li[15]/a

# 질병
# //*[@id="contents"]/div[3]/div/div[1]/ul/li[1]/article/section/a/div/h3
# //*[@id="contents"]/div[3]/div/div[1]/ul/li[2]/article/section/a/div/h3
# //*[@id="contents"]/div[3]/div/div[1]/ul/li[4]/article/section/a/div/h3
# //*[@id="contents"]/div[3]/div/div[1]/ul/li[60]/article/section/a/div/h3
# //*[@id="contents"]/div[3]/div/div[1]/ul/li[70]/article/section/a/div/h3

# 내용
# //*[@id="contents"]/section[1]/div[2]/article/section
# //*[@id="contents"]/section[1]/div[2]/article/section
# //*[@id="contents"]/section[1]/div[2]/article/section


# URL
# http://www.samsunghospital.com/home/healthInfo/content/contentList.do?CONT_CLS_CD=001020001001&TAB=DIS_CATE

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
from selenium.webdriver.common.keys import Keys


options = webdriver.ChromeOptions()
# options.add_argument('headless')  # 크롤링하는 웹 브라우저를 볼 수 없음
# options.add_argument('window-size=1920x1080')
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")  # 브라우저 보려면 여기까지 주석
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)


try:
    url = 'http://www.samsunghospital.com/home/healthInfo/content/contentList.do?CONT_CLS_CD=001020001001&TAB=DIS_CATE'
    driver.get(url)
    for i in range(1, 16):
        disease_page_xpath = '//*[@id="tab-panel-search-type01"]/div/div/ul/li[{}]/a'.format(i)
        driver.find_element_by_xpath(disease_page_xpath).click()
        time.sleep(1)
        diseases = []
        contents = []
        for j in range(1, 71):
            try:
                disease_name_xpath = '//*[@id="contents"]/div[3]/div/div[1]/ul/li[{}]/article/section/a'.format(j)

                content_rink = driver.find_element_by_xpath(disease_name_xpath).get_attribute('href')
                driver.get(content_rink)
                time.sleep(1)
                disease = driver.find_element_by_xpath('//*[@id="contents"]/section[1]/div[2]/article/header/h1/strong').text
                content = driver.find_element_by_xpath('//*[@id="contents"]/section[1]/div[2]/article/section').text

                diseases.append(disease)
                contents.append(content)
                driver.back()
                time.sleep(0.2)

            except:
                print('{}page_{}_error'.format(i, j))
        df_content_100 = pd.DataFrame({'Disease':diseases, 'Content':contents})
        df_content_100.to_csv('./crawling_data/disease_samsung_{}.csv'.format(i), index=False)
except:
    print('totally error')
