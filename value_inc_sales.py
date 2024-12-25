##### LIBRARIES #####
import pandas as pd


##### LOADING DATASETS #####

# dataset of transactions
df = pd.read_csv('transactions.csv', sep = ';')

# dataset of seasons
df_seasons = pd.read_csv('value_inc_seasons.csv', sep = ';')


##### CLEANING AND TRANSFORMING DATA #####

# Adding new columns to dataframe

# cost per transactions
df['CostPerTransaction'] = df['CostPerItem'] * df['NumberOfItemsPurchased']

# sales per transactions
df['SalesPerTransaction'] = df['SellingPricePerItem'] * df['NumberOfItemsPurchased']

# profit = sales - cost
df['ProfitPerTransaction'] = df['SalesPerTransaction'] - df['CostPerTransaction'] 

# Markup = (Sales - Cost) / Cost
df['Markup'] = round(df['ProfitPerTransaction'] / df['CostPerTransaction'],2)

# converting month to number in df and df_seasons
df['Month'] = pd.to_datetime(df['Month'], format='%b').dt.month
df_seasons['Month'] = pd.to_datetime(df_seasons['Month'], format='%b').dt.month

# creating a date column
df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

# using split to split the client_keywords field
split_col = df['ClientKeywords'].str.split(',', expand = True)

# creating new columns for the split columns
df['ClientAge']  = split_col[0]
df['ClientType'] = split_col[1]
df['LenghtofContract'] = split_col[2]

# using the replace function
df['ClientAge'] = df['ClientAge'].str.replace('[', '', regex=False)
df['LenghtofContract'] = df['LenghtofContract'].str.replace(']', '', regex=False)

# using the lower case function to change item to lowercase
df['ItemDescription'] = df['ItemDescription'].str.lower()

# merging df and df _seasons
df = pd.merge(df, df_seasons, on='Month')

# droping irrelevant columns
df = df.drop(['ClientKeywords','Day','Year','Month'], axis = 1)


##### SAVING THE NEW DATAFRAME #####
df.to_csv('ValueInc_Cleaned.csv', index = False)