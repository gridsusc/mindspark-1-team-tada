#%%
import pandas as pd
import seaborn as sns
import missingno as msno

#%%
df = pd.read_csv('WDI_csv/WDIData.csv')
df1 = pd.read_csv('population-density-vs-prosperity.csv')
df2 = pd.read_csv('API_NY/API_NY.GDP.PCAP')
# %%
df1.columns
# %%
clean = df.dropna(axis = 1)
clean

#%%
msno.bar(df1)

# %%
msno.matrix(df1)

# %%
df1 = df1.rename(columns = {"GDP per capita, PPP (constant 2017 international $)" : 'GDP'})
# %%
df1['GDP']
# %%
