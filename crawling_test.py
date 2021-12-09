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

try:
    for i in range(1, 2):
        url = 'https://www.cancer.go.kr/lay1/program/S1T211C223/cancer/list.do?page={}'.format(i)
        Disease = []
        Content = []
        for j in range(1, 100):
            print(j, '번째 크롤링 중')
            try:
                driver.get(url)
                cancer_xpath = '//*[@id="cancerList"]/ul/li[{}]/a/span[1]'.format(j)
                cancer_button_xpath = '//*[@id="cancerList"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(cancer_xpath).text
                print(title)
                driver.find_element_by_xpath(cancer_button_xpath).click()
                try:
                    content = driver.find_element_by_xpath('//*[@id="div_page"]').text
                    Disease.append(title)
                    Content.append(content)
                except:
                    print('main text error')
            except:
                print('error')

            df_content = pd.DataFrame({'Disease':Disease, 'Content':Content})
            df_content.to_csv('./crawling/disease_{}.csv'.format('cancer'), index=False)

except:
    print('totally error')


#//*[@id="cancerList"]/ul/li[1]/a
#//*[@id="cancerList"]/ul/li[2]/a



#//*[@id="div_page"]
#//*[@id="div_page"]
#
# //*[@id="cancerList"]/ul/li[1]/a/span[1]
# //*[@id="cancerList"]/ul/li[1]/a

#//*[@id="div_page"]
#//*[@id="div_page"]
#//*[@id="div_page"]
