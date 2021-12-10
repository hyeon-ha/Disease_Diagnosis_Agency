import pandas as pd
from konlpy.tag import Okt
import re

# df = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
# print(df.head())
# df.info()
# stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)
# stopwords.info()
# cleaned_sentences = []
# for cleaned_sentence in df.cleaned_sentences:
#     cleaned_sentence_words = cleaned_sentence.split()
#     words = []
#     for word in cleaned_sentence_words:
#         if word not in list(stopwords['stopword']): words.append(word)
#     cleaned_sentence = ' '.join(words)
#     cleaned_sentences.append(cleaned_sentence)
# df['cleaned_sentences'] = cleaned_sentences
# df.to_csv('./crawling_data/cleaned_review_2015_2021.csv', index=False)
# exit()

df = pd.read_csv('./crawling_data/Disease_content_onesentence.csv')
print(df.head())

okt = Okt()
stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)
stopwords = list(stopwords['stopword'])
add_stopwords = ['암이란', '발생부위', '정의', '종류', '관련통계', '예방', '위험요인', '예방법', '조기검진', '진단', '일반적증상', '진단방법', '진행단계', '설명', '관련',
                 '감별진단', '치료', '치료방법', '치료의', '부작용', '치료현황', '생활가이드', '일상생활', '식생활', '요약설명', '이란', '질병분류', '통계',
                 '업데이트', '발생현황', '바로가기', '유입사례', '발생보고', '정책정보', '감염병위기대응', '신종감염병현황', '보건소', '임상증상', '역학적', '방법',
                 '연관성', '개요', '원인병원체', '임상양상', '잠복기', '분석방법', '진단용', '검체', '전파관리', '조기치료', '신고', '기준', '신고시기', '신고방법', '담당부서',
                 '요인', '검진', '일반', '증상', '현황', '가이드', '요약', '어떻다', '의하다']
stopwords = stopwords + add_stopwords

count = 0
cleaned_contents = []
for content in df.Content:
    count += 1
    if count % 10 == 0: print('.', end='')
    if count % 100 == 0: print()
    content = re.sub('[^가-힣a-zA-Z ]', '', content)
    token = okt.pos(content, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective')]  # 명사, 동사, 부사만 활용한다.

    words = []
    for word in df_cleaned_token['word']:
        if (len(word) > 1 or word == '암') and word not in stopwords: words.append(word)

    cleaned_content = ' '.join(words)
    cleaned_contents.append(cleaned_content)

df['cleaned_content'] = cleaned_contents
print(df.head())
df.info()
df = df[['Disease', 'cleaned_content']]
df.to_csv('./crawling_data/cleaned_disease_content.csv', index=False)