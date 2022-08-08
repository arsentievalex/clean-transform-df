import pandas as pd


# read csv
df = pd.read_csv("raw.csv")


# clean product names
df.loc[df['Product Name'].str.contains('Apple', case=False), 'Product Name'] = 'Apple'
df.loc[df['Product Name'].str.contains('Samsung', case=False), 'Product Name'] = 'Samsung'
df.loc[df['Product Name'].str.contains('Huawei', case=False), 'Product Name'] = 'Huawei'
df.loc[df['Product Name'].str.contains('Microsoft', case=False), 'Product Name'] = 'Microsoft'
df.loc[df['Product Name'].str.contains('Google', case=False), 'Product Name'] = 'Google'


# define products to exclude
skus_to_drop = ['Android', 'Dell']


# remove rows with excluded products
for i in skus_to_drop:
    df.drop(df.index[df['Product Name'] == i], inplace=True)


# drop duplicates
df_no_duplicates = df.drop_duplicates(subset=['Customer Number', 'Product Name'])



# pivot df from long to wide format
df_no_duplicates = df_no_duplicates.pivot(index='Customer Number', columns='Product Name', values='Product Name')

# create new column and concatenate all other columns separated by ;
df_no_duplicates['Products Clean'] = df_no_duplicates.fillna('none').astype(str).apply('; '.join, axis=1)

# remove none values and unnecessary characters
df_no_duplicates = df_no_duplicates.replace('none; ', '', regex=True)
df_no_duplicates = df_no_duplicates.replace('none', '', regex=True)
df_no_duplicates['Products Clean'] = df_no_duplicates['Products Clean'].str.strip()
df_no_duplicates['Products Clean'] = df_no_duplicates['Products Clean'].str.rstrip(';')


# export output to xlsx
df_to_export = df_no_duplicates['Products Clean']
df_to_export.to_excel('data clean.xlsx')

