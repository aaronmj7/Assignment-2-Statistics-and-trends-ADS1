# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 00:25:50 2023

@author: aaron
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("electricity from coal.csv", skiprows=4)
df.drop(["Country Code", "Indicator Code", "Indicator Name"], axis=1,
        inplace=True)
df.dropna(how='all', axis=1, inplace=True)
df.set_index('Country Name', inplace=True)
df.columns.name = "Years"
df_trans = df.T
print(df, df_trans)
