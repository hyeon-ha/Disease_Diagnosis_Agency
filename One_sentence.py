import pandas as pd

df = pd.read_csv('./crawling_data/disease_all_index.csv', index_col=0)
one_contents = []
for disease in df['Disease'].unique():
    temp = df[df['Disease'] == disease]
    temp = temp['Content']
    one_sentence = ' '.join(temp)
    one_contents.append(one_sentence)
df_one_contents = pd.DataFrame({'Disease' : df['Disease'].unique(), 'Content' : one_contents})
print(df_one_contents.head())
print(df_one_contents.info())
df_one_contents.to_csv('./crawling_data/Disease_content_onesentence.csv', index=False)
