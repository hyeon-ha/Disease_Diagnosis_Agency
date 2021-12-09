from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
# options.add_argument('headless')  # 크롤링하는 웹 브라우저를 볼 수 없음
# options.add_argument('window-size=1920x1080')
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")  # 브라우저 보려면 여기까지 주석
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)

# //*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[1]/a
# //*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[99]/a
# //*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[6]
try:
    url = 'https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoMain.do?lclasSn=1'
    driver.get(url)
    for i in range(1, 7):
        disease_page_xpath = '//*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[{}]'.format(i)
        driver.find_element_by_xpath(disease_page_xpath).click()
        time.sleep(0.2)
        diseases = []
        contents = []
        for j in range(1, 100):
            try:
                disease_name_xpath = '//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[{}]/a'.format(j)
                disease = driver.find_element_by_xpath(disease_name_xpath).text
                new_tap_url = driver.find_element_by_xpath(disease_name_xpath).get_attribute('href')
                tap_temp = new_tap_url.split(':')
                if tap_temp[0] in ['http', 'https']:  # 새창일 경우
                    new_tap_url = driver.find_element_by_xpath(disease_name_xpath).get_attribute('href')
                    driver.get(new_tap_url)
                    time.sleep(0.2)
                    content = driver.find_element_by_xpath('//*[@id="tab1"]').text
                else:
                    driver.find_element_by_xpath(disease_name_xpath).click()
                    time.sleep(0.2)
                    content = driver.find_element_by_xpath('//*[@id="contentsDiv1"]').text
                diseases.append(disease)
                contents.append(content)
                driver.back()
                time.sleep(0.2)
            except:
                print('{}page_{}_error'.format(i, j))
        df_content_100 = pd.DataFrame({'Disease':diseases, 'Content':contents})
        df_content_100.to_csv('./crawling_data/disease_health_{}.csv'.format(i), index=False)
except:
    print('totally error')