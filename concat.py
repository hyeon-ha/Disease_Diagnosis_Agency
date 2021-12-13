import pandas as pd
import glob

d1 = pd.read_csv('./crawling/disease_asan_1.csv')
d2 = pd.read_csv('./crawling/disease_asan_3.csv')
d3 = pd.read_csv('./crawling/disease_asan_4.csv')
d4 = pd.read_csv('./crawling/disease_asan_5.csv')
d5 = pd.read_csv('./crawling/disease_asan_6.csv')
d6 = pd.read_csv('./crawling/disease_asan_7.csv')
d7 = pd.read_csv('./crawling/disease_asan_8.csv')
d8 = pd.read_csv('./crawling/disease_asan_9.csv')
d9 = pd.read_csv('./crawling/disease_asan_10.csv')
d10 = pd.read_csv('./crawling/disease_asan_11.csv')
d11 = pd.read_csv('./crawling/disease_asan_12.csv')
d12 = pd.read_csv('./crawling/disease_asan_13.csv')
d13 = pd.read_csv('./crawling/disease_asan_14.csv')
d14 = pd.read_csv('./crawling/disease_asan_15.csv')
d15 = pd.read_csv('./crawling/disease_asan_16.csv')
d16 = pd.read_csv('./crawling/disease_asan_17.csv')
d17 = pd.read_csv('./crawling/disease_asan_18.csv')
d18 = pd.read_csv('./crawling/disease_asan_19.csv')
d19 = pd.read_csv('./crawling/disease_asan_20.csv')

df = pd.concat([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19], ignore_index=True)

df.to_csv('./crawling/disease_asan.csv', index = False)
