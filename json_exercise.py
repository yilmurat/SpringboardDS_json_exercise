# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:15:31 2018

@author: myildirim
"""
import pandas as pd
import json
from pandas.io.json import json_normalize

#Exercise 1 : Find the 10 countries with most projects
#Read the json file and get top10 using value_counts method on countryname column

json_df = pd.read_json('../data_wrangling_json/data/world_bank_projects.json')
country_counts = json_df.countryname.value_counts()
print(country_counts[:10])

#Exercise 2: Find the top 10 major project themes (using column 'mjtheme_namecode')
#Load the json file, normalize it with json_normalize using column mjtheme_namecode
#and get the top 10 using value counts.

test_df = json.load((open('../data_wrangling_json/data/world_bank_projects.json')))
print(json_normalize(test_df,'mjtheme_namecode').name.value_counts().head(10))

#Exercise 3 : Create a dataframe with the missing names filled in.

# normalize the dataframe using mjtheme_namecode
norm_df = json_normalize(test_df,'mjtheme_namecode')

#Create a new dataframe to store code-name pairs
df_codename2 = pd.DataFrame(columns=['code','name'])

#Read the normalized dataframe and fill dataframe created above with code-name pairs
for i in range(len(list(norm_df['code']))):
    if norm_df['name'][i] != "":
        df_codename2 = df_codename2.append({'code':norm_df['code'][i],'name':norm_df['name'][i]},ignore_index=True).drop_duplicates()

#reindex so that code column is the index
df_codename2_i = df_codename2.set_index('code')

# fill the missing values in the dataframe
for i in range(len(json_df.mjtheme_namecode)):
    for j in range(len(json_df.mjtheme_namecode[i])):
        if json_df.mjtheme_namecode[i][j]['name'] == '' :
            json_df.mjtheme_namecode[i][j]['name'] = df_codename2_i.loc[str(json_df.mjtheme_namecode[i][j]['code']),'name']
            
            