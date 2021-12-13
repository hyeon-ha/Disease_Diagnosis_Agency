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
for i in range(len(df)):
    df['Disease'][i] = re.sub(regex_0, '', df['Disease'][i])
    df['Disease'][i] = re.sub(regex_1, '', df['Disease'][i])
    temp = df['Disease'][i]
    for j in range(len(temp) - 5):
        if 65 <= ord(temp[j]) <= 122:
            count = 0
            for k in range(j, len(temp) - 5):
                if 65 <= ord(temp[k]) <= 122: count += 1
                else: break
            if count >= 5:
                df['Disease'][i] = temp[:j]
                break
df["Disease"] = df["Disease"].str.replace(pat=r'[^가-힣A-Za-z0-9]', repl=r'', regex=True)
df = df[['Disease', 'Content']]
df.info()
df.to_csv('./crawling_data/disease_all_index.csv')