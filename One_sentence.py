import pandas as pd

df = pd.read_csv('./crawling_data/naver_movie_reviews_2015_2021.csv')
one_sentences = []
for title in df['title'].unique():  # 리뷰 여러개를 하나로 통합시킨다.
    temp = df[df['title'] == title]
    temp = temp['reviews']
    one_sentence = ' '.join(temp)  # 해당 영화의 리뷰들을 하나로 합친다.
    one_sentences.append(one_sentence)
df_one_sentences = pd.DataFrame({'titles' : df['title'].unique(), 'reviews' : one_sentences})
print(df_one_sentences.head())
df_one_sentences.to_csv('./crawling_data/naver_movie_reviews_onesentence_2015_2021.csv', index=False)
