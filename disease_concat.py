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
    df_temp.to_csv(data_path, index=False)
    df = pd.concat([df, df_temp])
df.drop_duplicates(inplace=True)
df.reset_index(inplace=True)
print(df.head())
df["Disease"] = df["Disease"].str.replace(pat=r'[^\w]', repl=r'', regex=True)

df.info()
df.to_csv('./crawling_data/disease_all_index.csv', index=False)