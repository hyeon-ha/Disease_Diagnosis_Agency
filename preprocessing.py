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

df = pd.read_csv('./crawling_data/naver_movie_reviews_onesentence_2015_2021.csv')
print(df.head())

okt = Okt()
stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)
stopwords = list(stopwords['stopword'])

count = 0
cleaned_sentences = []
for content in df.Content:
    count += 1
    if count % 10 == 0: print('.', end='')
    if count % 100 == 0: print()
    content = re.sub('[^가-힣a-zA-Z ]', '', content)  # 한글만 제외하고 나머지는 모두 없앤다.
    token = okt.pos(content, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective')]  # 명사, 동사, 부사만 활용한다.

    words = []
    for word in df_cleaned_token['word']:
        if len(word) > 1 and word not in stopwords: words.append(word)

    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
print(df.head())
df.info()
df = df[['titles', 'cleaned_sentences']]  # == df.drop('reviews', inplace=True, axis=1)
df.to_csv('./crawling_data/cleaned_review_2015_2021.csv', index=False)