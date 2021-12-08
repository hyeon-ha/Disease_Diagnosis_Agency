# crawling 작업

# 3명이 각자 한 링크씩 맡아서 크롤링 작업을 진행하겠습니다.
# 컬럼명은 ['Disease', 'Symptom']로 진행합니다.
# 파일명은 'disease_{}.csv'.format('health', 'cancer', 'epidemic')으로 해주세요.
# 질병 및 장애 : https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoMain.do?lclasSn=1
# //*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[1]/a  맨 처음
# //*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[2]/a
# //*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[99]/a
# 2, 5, 6페이지의 일부 질병은 새창으로 열어지니 대책 필요
# 암 : https://www.cancer.go.kr/lay1/program/S1T211C223/cancer/list.do
# //*[@id="cancerList"]/ul/li[1]/a/span[1]
# //*[@id="cancerList"]/ul/li[2]/a/span[1]
# //*[@id="cancerList"]/ul/li[3]/a/span[1]
# //*[@id="cancerList"]/ul/li[99]/a/span[1]
# 증상 : //*[@id="cancerMenu"]/ul[4]/li[2]/a
# 증상 내용 : //*[@id="div_page"]/p
# 감염병 : https://www.kdca.go.kr/npt/biz/npp/portal/nppLwcrIcdMain.do#042ND0614
# //*[@id="gTd"]/a[1]  가
# //*[@id="gTd"]/a[2]
# //*[@id="nTd"]/a[1]  나
# //*[@id="dTd"]/a[1]  다
# //*[@id="contentDiv"]/p[18]/font/span[2]
# //*[@id="contentDiv"]/span/font/span/p[9]
# 크롤링 완료한 데이터는 아래 링크로 올려주세요
# https://drive.google.com/drive/folders/1vKfj3i94UTzqGQKzQ8DwtW0LXsDiK2Qb?usp=sharing
# 우선 테스트 파이썬 파일 각 이니셜 별로 만들어서 풀리퀘스트 테스트 부탁드립니다.

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
import requests
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)
# 파일의 요소를 class를 따오면 된다
# webpage = requests.get("https://www.kdca.go.kr/npt/biz/npp/portal/nppLwcrIcdMain.do#042ND0204")
# soup = BeautifulSoup(webpage.content,"html.parser")
#
# print(soup)
# # <a href="javascript:fn_sumryMain('ND0204','04');" class="btn-list" data-icdcd="ND0204">•간흡충증</a>
# < ahref = "javascript:fn_sumryMain('NB0001','02');"class ="btn-list" data-icdcd="NB0001" > •결핵 < / a >
#
# < a
# href = "javascript:fn_sumryMain('NA0003','01');"
# class ="btn-list" data-icdcd="NA0003" > •라싸열 < / a >
# Disease_Diagnosis_class = ' '
# url = 'https://www.kdca.go.kr/npt/biz/npp/portal/nppLwcrIcdMain.do#042ND0614'
# titles = []
# reviews = []
# try :
#     driver.get(url)
#     crawling_disease_health = ''
# 첫번째 <a href="javascript:fn_sumryMain('NA0001','01');" class="btn-list" data-mainicdcd="NA0001">에볼라바이러스병</a>
# 두번쨰 <a href="javascript:fn_sumryMain('NA0003','01');" class="btn-list" data-mainicdcd="NA0003">라싸열</a>
# 1급   // *[ @ id = "tabs-1"] / div[2] / div / div / div / table / tbody / tr[1] / td[1] / a
#    // *[ @ id = "tabs-1"] / div[2] / div / div / div / table / tbody / tr[2] / td[1] / a
#    // *[ @ id = "tabs-1"] / div[3] / div / div / div / table / tbody / tr[1] / td[1] / a
# 4급   // *[ @ id = "tabs-1"] / div[5] / div / div / div / table / tbody / tr[62] / td[1] / a
#    // *[ @ id = "tabs-1"] / div[5] / div / div / div / table / tbody / tr[1] / td[1] / a

try:
    url = 'https://www.kdca.go.kr/npt/biz/npp/portal/nppLwcrIcdMain.do#011NA0001'
    Diseases = []
    Symptom = []
    for i in range(2,6):
        try:
            for i in range(1,63):
                driver.get(url)
                disease_class_xpath = '// *[ @ id = "tabs-1"] / div[{}] / div / div / div / table / tbody / tr[{}] / td[1] / a'.format(i,j)
                disease = driver.find_element_by_xpath(disease_class_xpath).text
                Diseases.append(disease)
                driver.find_element_by_xpath(disease_class_xpath).click()

except:
    print(error)
df_disease = pd.DataFrame{'Diseas':}
