import pandas as pd

df = pd.read_csv('./crawling_data/naver_movie_reviews_2015_2021.csv')
one_sentences = []
for disease in df['Disease'].unique():
    temp = df[df['Disease'] == disease]
    temp = temp['Content']
    one_sentence = ' '.join(temp)
    one_sentences.append(one_sentence)
df_one_sentences = pd.DataFrame({'Disease' : df['Disease'].unique(), 'Content' : one_sentences})
print(df_one_sentences.head())
df_one_sentences.to_csv('./crawling_data/Disease_content_onesentence.csv', index=False)
