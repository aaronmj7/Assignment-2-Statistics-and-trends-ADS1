# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 00:25:50 2023

@author: aaron
"""

import pandas as pd
import matplotlib.pyplot as plt


def dataframe(file_name, countries, years):
    df = pd.read_csv(file_name, skiprows=4)
    df.drop(["Country Code", "Indicator Code", "Indicator Name"], axis=1,
            inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    df.set_index(['Country Name'], inplace=True)
    df.index.rename("Country", inplace=True)
    df.columns.name = "Years"
    df = df.loc[countries, years]
    df_t = df.transpose()
    return df, df_t


countries = ["India", "Japan", "Australia", "China", "United States",
             "Russian Federation", "United Kingdom"]
years = [str(i) for i in range(1990, 2016)]
df, df_t = dataframe("electricity from oil,gas,coal.csv", countries, years)
df_t.plot()
plt.show()

co, co_t = dataframe("co2 emission per capita.csv", countries, years)
co_t.plot()
plt.show()

years = [str(i) for i in range(1990, 2016, 5)]

nu, nu_t = dataframe("electricity from nuclear.csv", countries, years)
nu.plot.bar()
plt.show()

rn, rn_t = dataframe("Electricity from renewable ex hydro.csv", countries,
                     years)
hy, hy_t = dataframe("Electricity from hydro.csv", countries, years)
rn.add(hy).plot.bar()
plt.show()
