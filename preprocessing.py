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
add_stopwords = ['암이란', '발생부위', '정의', '종류', '관련통계', '예방', '위험요인', '예방법', '조기검진', '진단', '일반적증상', '진단방법', '진행단계',
                 '감별진단', '치료', '치료방법', '치료의', '부작용', '재발', '치료현황', '생활가이드', '일상생활', '식생활', '요약설명', '이란']
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