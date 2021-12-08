import pandas as pd

df = pd.read_csv('./crawling_data/naver_movie_reviews_2015_2021.csv')
one_sentences = []
for disease in df['Disease'].unique():  # 리뷰 여러개를 하나로 통합시킨다.
    temp = df[df['Disease'] == disease]
    temp = temp['Content']
    one_sentence = ' '.join(temp)  # 해당 영화의 리뷰들을 하나로 합친다.
    one_sentences.append(one_sentence)
df_one_sentences = pd.DataFrame({'Disease' : df['Disease'].unique(), 'Content' : one_sentences})
print(df_one_sentences.head())
df_one_sentences.to_csv('./crawling_data/Disease_content_onesentence.csv', index=False)
