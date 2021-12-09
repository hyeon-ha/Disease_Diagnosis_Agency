#김영준 테스트파일입니다.
#https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoMain.do?lclasSn=1
# 3명이 각자 한 링크씩 맡아서 크롤링 작업을 진행하겠습니다.
# 컬럼명은 ['Disease', 'Symptom']로 진행합니다.
# 파일명은 'disease_{}.csv'.format('health', 'cancer', 'epidemic')으로 해주세요.

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

symptom_button_xpath = '//*[@id="cancerMenu"]/ul[4]/li[2]/a'
symptom_text_xpath = '//*[@id="div_page"]/p'

#name : //*[@id="cancerList"]/ul/li[1]/a/span[1]
#//*[@id="cancerList"]/ul/li[2]/a/span[1]
#//*[@id="cancerList"]/ul/li[3]/a/span[1]
#//*[@id="cancerList"]/ul/li[99]/a/span[1]

#자세히보기 :  //*[@id="cancerList"]/ul/li[1]/a
#//*[@id="cancerList"]/ul/li[2]/a
#//*[@id="cancerList"]/ul/li[3]/a
#//*[@id="cancerList"]/ul/li[99]/a

#일반적증상버튼 : //*[@id="cancerMenu"]/ul[4]/li[2]/a
#//*[@id="cancerMenu"]/ul[4]/li[2]/a
#//*[@id="cancerMenu"]/ul[4]/li[2]/a
#//*[@id="cancerMenu"]/ul[4]/li[2]/a

#일반적증상텍스트 : //*[@id="div_page"]/p
#//*[@id="div_page"]/p[3]

#//*[@id="div_page"]
#//*[@id="div_page"]
#//*[@id="div_page"]
try:
    for i in range(1, 2):
        url = 'https://www.cancer.go.kr/lay1/program/S1T211C223/cancer/list.do?page={}'.format(i)
        Disease = []
        Symptom = []
        for j in range(1, 5):
            print(j, '번째 크롤링 중')
            try:
                driver.get(url)
                cancer_xpath = '//*[@id="cancerList"]/ul/li[{}]/a/span[1]'.format(j)
                title = driver.find_element_by_xpath(cancer_xpath).text
                print(title)
                driver.find_element_by_xpath(cancer_xpath).click()
                # if driver.find_element_by_xpath(symptom_button_xpath).text == '일반적증상':
                #     driver.find_element_by_xpath(symptom_button_xpath).click()
                #     Symptom = driver.find_element_by_xpath('//*[@id="div_page"]/p')
                #     print(Symptom)
                #     time.sleep(0.5)
#                 driver.get(symptom_page_url)
#                 review_range = driver.find_element_by_xpath(review_number_xpath).text
#                 review_range = review_range.replace(',', '')
#                 review_range = int(review_range)
#                 review_range = review_range // 10 + 2
#                 if review_range > 6: review_range = 6
#                 for k in range(1, review_range):
#                     driver.get(review_page_url + '&page={}'.format(k))
#                     #time.sleep(0.3)
#                     for l in range(1, 11):
#                         review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
#                         try:
#                             driver.find_element_by_xpath(review_title_xpath).click()
#                             #time.sleep(0.3)
#                             review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
#                             # print('===================== =====================')
#                             # print(title)
#                             # print(review)
#                             titles.append(title)
#                             reviews.append(review)
#                             driver.back()
#                         except:
#                             # print(l, '번째 review가 없다.')
#                             break
#
            except:
                print('error')
        df_review_20 = pd.DataFrame({'Disease':Disease, 'Symptom':Symptom})
        df_review_20.to_csv(
            './crawling/disease_{}.csv'.format('cancer'),
            index=False)
        # 파일명은 'disease_{}.csv'.format('health', 'cancer', 'epidemic')으로 해주세요.
#'Disease', 'Symptom'
except:
    print('totally error')
finally:
    driver.close()
# # df_review = pd.DataFrame({'title':titles, 'reviews':reviews})
# # df_review.to_csv('./crawling_data/reviews_{}.csv'.format(2020))






