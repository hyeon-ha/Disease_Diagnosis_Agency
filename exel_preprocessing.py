import pandas as pd

e_index = ['Inspection_standard', 'Inspection_items', 'required_Inspection']
df = pd.read_excel('./crawling_data/rare_disease_process.xlsx', engine = 'openpyxl')
print(df.head())
print(df.info())
contents = []
print(len(df))
for i in range(len(df)):
    content = ''
    for j in e_index:
        if str(df.iloc[i][j]) != 'nan':
            content = content + str(df.iloc[i][j])
    contents.append(content)
    if i % 10 == 0: print('.', end='')
    if i % 100 == 0: print('')
df['Content'] = contents
print(df.head())
df = df[['Disease', 'Content']]
df.info()
df.to_csv('./crawling_data/team_crawling/rare_disease_content.csv', index=False)