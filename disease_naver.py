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
All_disease = []
All_content = []
diseases = []
contents = []
try:
    for i in range(1, 191):
        url = 'https://terms.naver.com/list.naver?cid=40942&categoryId=32773&so=st3.asc&viewType=&categoryType=&page={}'.format(i)
        driver.get(url)
        time.sleep(0.2)
        for j in range(1, 16):
            try:
                driver.find_element_by_xpath('//*[@id="content"]/div[4]/ul/li[{}]/div/div[1]/strong/a[1]'.format(j)).send_keys(Keys.ENTER)
                time.sleep(0.3)
                disease = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/h2').text
                content = driver.find_element_by_xpath('//*[@id="size_ct"]').text
                diseases.append(disease)
                contents.append(content)
                print('{}번째 내용 로드'.format((i - 1) * 15 + j))
            except:
                print('{}번째 내용 로드 실패'.format((i - 1) * 15 + j))
            driver.back()
            time.sleep(0.3)

        if i % 20 == 0:
            df_content = pd.DataFrame({'Disease': diseases, 'Content': contents})
            print(df_content.info())
            df_content.to_csv('./crawling_data/team_crawling/disease_naver_{}.csv'.format(i//20), index=False)
            diseases = []
            contents = []
except:
    print('totally error')
finally:
    driver.close()