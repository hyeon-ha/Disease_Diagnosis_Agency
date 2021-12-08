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


def crawlData(driver, year):
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
    exit()
    traceback_filename = f'traceback_{datetime.now().strftime("%y%m%d-%H%M%S")}.txt'
    url = 'https://www.kdca.go.kr/npt/biz/npp/portal/nppLwcrIcdMain.do'
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="tab2"]').click()

    # ㄱ: //*[@id="tabs-2"]/div/ul/li[1]/a
    # ㄴ: //*[@id="tabs-2"]/div/ul/li[2]/a
    id_list = []
    for i in range(1, 16):
        button_path = f'//*[@id="tabs-2"]/div/ul/li[{i}]/a'
        id_list.append(driver.find_element_by_xpath(button_path).get_attribute('href').split('#')[-1])

    print(f'id_list: {id_list}')
    for id_val in id_list:
        disease_list = driver.find_element_by_xpath(f'//*[@id="{id_val}"]').text.split('\n')
        for j in range(1, len(disease_list) + 1):
            driver.find_element_by_xpath(f'//*[@id="{id_val}"]/a[{j}]').click()
            time.sleep(1)
            driver.back()
            time.sleep(1)
        print(disease_list)
        print(len(disease_list))
    # driver.close()
    exit()
    # <font face="맑은 고딕">증상</font>


    # 연도에 맞는 페이지와 영화 갯수를 획득하기 위한 과정
    driver.get(url)
    for i in range(1, 11):
        if i != 10:
            for j in range(1, 5):
                find_xpath = driver.find_element_by_xpath(f'//*[@id="old_content"]/table/tbody/tr[{i}]/td[{j}]').text
                if year == find_xpath.split()[0]:
                    items = find_xpath.split()[1].replace('(', '').replace(')', '')
                    break
        else:
            for j in range(1, 3):
                find_xpath = driver.find_element_by_xpath(f'//*[@id="old_content"]/table/tbody/tr[{i}]/td[{j}]').text
                if year == find_xpath.split()[0]:
                    items = find_xpath.split()[1].replace('(', '').replace(')', '')
                    break

    movie_pages = int(items) // 20 + 2
    count = 0
    # 해당 연도의 영화 페이지로 이동

    for i in range(1, movie_pages):
        try:
            url = f'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}&page={i}'
            driver.get(url)
            time.sleep(0.2)
            movie_title_range = 21 if i != movie_pages - 1 else int(items) % 20 + 1
            for j in range(1, movie_title_range):
                error_count = 0
                count += 1
                start_time = time.time()
                # 영화 제목(title) 클릭
                title = driver.find_element_by_xpath(f'//*[@id="old_content"]/ul/li[{j}]/a').text
                driver.find_element_by_xpath(f'//*[@id="old_content"]/ul/li[{j}]/a').click()
                # 리뷰 버튼의 위치를 찾아 인덱스를 반환하기 위한 목적
                check_elements = driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]').text.split()
                for k in range(len(check_elements)):
                    if '리뷰' == check_elements[k]:
                        review_button_xpath = f'//*[@id="movieEndTabMenu"]/li[{k + 1}]/a/em'
                        break
                # 리뷰 버튼 클릭
                time.sleep(0.2)
                driver.find_element_by_xpath(review_button_xpath).click()
                # 리뷰 건 수 확인
                review_count = driver.find_element_by_xpath('//*[@id="reviewTab"]/div/div/div[2]/span/em').text
                review_count = review_count.replace(',', '')
                review_count = int(review_count)
                # 리뷰의 건수가 6개를 초과할 경우, 데이터가 너무 많아져서 6개만 가져오고자 한다.
                review_count = 6 if review_count > 6 else review_count
                for k in range(1, review_count + 1):
                    try:
                        # 리뷰 클릭
                        time.sleep(0.2)
                        driver.find_element_by_xpath(f'//*[@id="reviewTab"]/div/div/ul/li[{k}]/a/strong').click()
                        # 리뷰 복사
                        time.sleep(0.2)
                        review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                        # 리뷰 리스트로 복귀
                        time.sleep(0.2)
                        driver.back()
                    except Exception as E:
                        error_count += 1
                        driver.back()
                    else:
                        titles.append(title)
                        reviews.append(review)
                # 트레이스백(trackback)을 위한 디버그 및 파일 출력
                with open(f'./{traceback_filename}', 'a') as f:
                    if error_count:
                        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]\t{count:4d}/{int(items):4d} ({round(count / int(items), 4)})%\t\truntime is {(time.time() - start_time):.4f} seconds.\t{error_count} errors occurred.\n')
                        print(f'{count:4d}/{int(items):4d} ({round(count / int(items), 4)})%\t\truntime is {(time.time() - start_time):.4f} seconds.\t{error_count} errors occurred.')
                    else:
                        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]\t{count:4d}/{int(items):4d} ({round(count / int(items), 4)})%\t\truntime is {(time.time() - start_time):.4f} seconds.\n')
                        print(f'{count:4d}/{int(items):4d} ({round(count / int(items), 4)})%\t\truntime is {(time.time() - start_time):.4f} seconds.')
                driver.get(url)
                time.sleep(1)
            df_review_20 = pd.DataFrame({'titles': titles, 'reviews': reviews})
            df_review_20.to_csv(f'./crawling_data/reviews_{year}_{i}.csv', index=False)
            print(f'"reviews_{year}_{i}.csv" is saved.')
        except Exception as E:
            print(f'Unknown error occurred..\n{E}')
            with open(f'./{traceback_filename}', 'a') as f:
                f.write(f'Unknown error occurred..\n{E}\n')

    time.sleep(3)
    driver.close()
    exit()


if __name__ == '__main__':
    driver_option = initializeDriverOptions()
    crawlData(driver=driver_option, year='2016')
