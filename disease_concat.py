import re

import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/team_crawling/*')
print(data_paths)
df = pd.DataFrame()
for data_path in data_paths:
    df_temp = pd.read_csv(data_path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df_temp.columns = ['Disease', 'Content']
    df = pd.concat([df, df_temp])
df.drop_duplicates(inplace=True)
df.reset_index(inplace=True)
print(df.head())
print(df.tail())
regex_0 = '\(.*\)|\s-\s.*'
regex_1 = '\[.*\]|\s-\s.*'
df['Disease'] = df['Disease'].str.replace(' ','')
df["Disease"] = df["Disease"].str.replace(pat=r'[^가-힣A-Za-z0-9]', repl=r'', regex=True)
# for i in range(len(df)):
#     temp = df['Disease'][i]
#     for j in range(len(temp) - 5):
#         if 65 <= ord(temp[j]) <= 122:
#             count = 0
#             for k in range(j, len(temp) - 5):
#                 if ord(temp[k]) >= 65 and ord(temp[k]) <= 122: count += 1
#                 else: break
#             if count >= 5:
#                 df['Disease'][i] = temp[:j]
#                 print(i, df['Disease'][i])
#                 break
for i in range(len(df)):
    temp = df['Disease'][i]
    for j in range(len(temp)-1, -1, -1):
        if not(65 <= ord(temp[j]) <= 122):
            df['Disease'][i] = temp[:(j+1)]
            print(i, df['Disease'][i])
            break

df = df[['Disease', 'Content']]
df.info()
df.to_csv('./crawling_data/disease_all_index.csv')