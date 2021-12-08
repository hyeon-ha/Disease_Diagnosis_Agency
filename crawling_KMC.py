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
    driver = initializeDriverOptions()
    url = 'https://www.kdca.go.kr/npt/biz/npp/portal/nppSumryMain.do'
    driver.get(url)
    items = {'1급': 17, '2급': 22, '3급': 26, '4급': 62}
    disease_list = []
    for i in range(2, 6):
        iteration = items[f'{i - 1}급']
        for j in range(1, iteration + 1):
            xpath = f'//*[@id="tabs-1"]/div[{i}]/div/div/div/table/tbody/tr[{j}]/td[1]/a'
            disease_name = driver.find_element_by_xpath(xpath).text.replace('\n', '')
            driver.find_element_by_xpath(xpath).click()
            time.sleep(1)
            driver.back()
            time.sleep(1)
            # n = driver.find_element_by_xpath('//*[@id="contentDiv"]').text
            disease_list.append(disease_name)

    print(disease_list)
    driver.close()


if __name__ == '__main__':
    crawlData()
