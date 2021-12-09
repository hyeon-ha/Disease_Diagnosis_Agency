from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


def initializeDriverOptions():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')        # Web-browser가 뜨지 않는다.
    options.add_argument('window-size=1920x1080')
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    options.add_argument('lang=ko_KR')
    options.add_argument('disable_gpu')

    return webdriver.Chrome('./chromedriver', options=options)


def crawlData():
    start_time = time.time()
    driver = initializeDriverOptions()
    filename = 'disease_epidemic.csv'
    disease_list = []
    symptom_list = []
    items = {'1급': 17, '2급': 22, '3급': 26, '4급': 62}

    url = 'https://www.kdca.go.kr/npt/biz/npp/portal/nppSumryMain.do'
    driver.get(url)
    for i in range(2, 6):
        iteration = items[f'{i - 1}급']
        for j in range(1, iteration + 1):
            disease_xpath = f'//*[@id="tabs-1"]/div[{i}]/div/div/div/table/tbody/tr[{j}]/td[1]/a'
            disease_name = driver.find_element_by_xpath(disease_xpath).text.replace('\n', '')
            driver.find_element_by_xpath(disease_xpath).click()
            # 증상 등 내부 내용 크롤링
            symptom = driver.find_element_by_xpath('//*[@id="contentDiv"]').text
            time.sleep(0.5)
            driver.back()
            time.sleep(0.5)
            disease_list.append(disease_name)
            symptom_list.append(symptom)
    # 데이터 프레임 생성
    dataframe = pd.DataFrame({'Disease': disease_list, 'Content': symptom_list})
    # 파일(.csv) 저장
    dataframe.to_csv(f'./{filename}', index=False)
    print(f'"{filename}" is saved.\truntime is {time.time() - start_time:.3f} seconds')
    driver.close()


if __name__ == '__main__':
    crawlData()

