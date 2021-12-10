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
start_url = 'https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoMain.do?lclasSn=1'
url = 'https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoMain.do'


try:
    for i in range(1, 2):
        Disease = []
        Content = []
        driver.get(start_url)
        for k in range(1, 7): #페이지
            if k >= 2:
                driver.find_element_by_xpath('//*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[{}]'.format(k)).click()
            for j in range(1, 100): #데이터
                print(k, '-', j, '번째 크롤링 중')
                try:
                    disease_xpath = '//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[{}]/a'.format(j)
                    #cancer_button_xpath = '//*[@id="cancerList"]/ul/li[{}]/a'.format(j)
                    title = driver.find_element_by_xpath(disease_xpath).text
                    print(title)
                    driver.find_element_by_xpath(disease_xpath).click()
                    try:
                        content = driver.find_element_by_xpath('//*[@id="gnrlzHealthInfoViewForm"]/div[2]/div[2]').text
                        Disease.append(title)
                        Content.append(content)
                        driver.back()
                    except:
                        new_tap_url = driver.find_element_by_xpath(disease_xpath).get_attribute('href')
                        print('main text error')
                except:
                    print('error')
        df_content = pd.DataFrame({'Disease':Disease, 'Content':Content})
        df_content.to_csv('./crawling/disease_{}.csv'.format('health'), index=False)

except:
    print('totally error')


#1페이지
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[1]/a
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[2]/a
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[3]/a
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[99]/a

#2페이지
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[1]/a
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[2]/a
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[3]/a
#//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[99]/a

#페이지버튼
#//*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[1]
#//*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[2]
#//*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[3]
#//*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[6]

#내용
#//*[@id="gnrlzHealthInfoViewForm"]/div[2]/div[2]
#//*[@id="gnrlzHealthInfoViewForm"]/div[2]/div[2]
#//*[@id="gnrlzHealthInfoViewForm"]/div[2]/div[2]