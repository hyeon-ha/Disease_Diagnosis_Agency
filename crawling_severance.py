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
url = 'https://health.severance.healthcare/health/encyclopedia/disease/body_board.do'
diseases = []
contents = []
try:
    driver.get(url)
    for i in range(1, 284):
        if i == 110: continue
        a = i // 12
        for j in range(a):
            driver.find_element_by_xpath('//*[@id="btnMoreArticle"]').send_keys(Keys.ENTER)
            time.sleep(0.3)
        try:
            driver.find_element_by_xpath('//*[@id="cms-content"]/div/div/div[2]/div[{}]/a/div[2]/div[1]/strong'.format(i)).click()
            time.sleep(0.2)
            disease = driver.find_element_by_xpath('//*[@id="cms-content"]/div/div/div/div/div[1]/div/h3').text
            content = driver.find_element_by_xpath('//*[@id="cms-content"]/div/div/div/div/div[2]/div').text
            diseases.append(disease)
            contents.append(content)
            print('{}번째 내용 로드'.format(i))
        except:
            print('{}번째 내용 로드 실패'.format(i))
        driver.back()
        time.sleep(0.3)

    df_content = pd.DataFrame({'Disease': diseases, 'Content': contents})
    print(df_content.info())
    df_content.to_csv('./crawling_data/team_crawling/disease_severance.csv', index=False)
except:
    print('totally error')
finally:
    driver.close()