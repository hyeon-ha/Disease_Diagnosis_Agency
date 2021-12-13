from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('headless')  # 크롤링하는 웹 브라우저를 볼 수 없음
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")  # 브라우저 보려면 여기까지 주석
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)
diseases = []
contents = []
try:
    for i in range(1, 22):
        url = 'https://www.cmcseoul.or.kr/page/health/bible?p={}&s=10&q=%7B%22deptClsf%22%3A%22A%22%2C%22selectedDept%22%3A%22%22%2C%22hbDtContent%22%3A%22%22%2C%22exposeYn%22%3A%22Y%22%7D'.format(i)
        driver.get(url)
        time.sleep(0.5)
        for j in range(1, 11):
            try:
                driver.find_element_by_xpath('//*[@id="sub_section"]/div[3]/div/div[2]/ul/li[{}]/a/div/strong'.format(j)).click()
                time.sleep(1)
                disease = driver.find_element_by_xpath('//*[@id="sub_section"]/div[2]/h2').text
                content = driver.find_element_by_xpath('//*[@id="tabContent1"]/div[1]/div').text
                diseases.append(disease)
                contents.append(content)
                print('{}번째 내용 로드'.format((i - 1) * 10 + j))
            except:
                print('{}번째 내용 로드 실패'.format((i - 1) * 10 + j))
            driver.back()
            time.sleep(1)

        if i % 3 == 0:
            df_content = pd.DataFrame({'Disease': diseases, 'Content': contents})
            print(df_content.info())
            df_content.to_csv('./crawling_data/team_crawling/disease_catholic_{}.csv'.format(i//3), index=False)
            diseases = []
            contents = []
except:
    print('totally error')
finally:
    driver.close()