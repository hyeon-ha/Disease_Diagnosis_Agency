# crawling 작업

# 3명이 각자 한 링크씩 맡아서 크롤링 작업을 진행하겠습니다.
# 컬럼명은 ['Disease', 'Symptom']로 진행합니다.
# 파일명은 'disease_{}.csv'.format('health', 'cancer', 'epidemic')으로 해주세요.
# 질병 및 장애 : https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoMain.do
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

# 우선 테스트 파이썬 파일 각 이니셜 별로 만들어서 풀리퀘스트 테스트 부탁드립니다.

