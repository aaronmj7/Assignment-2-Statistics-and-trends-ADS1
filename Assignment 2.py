# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 00:25:50 2023

@author: aaron
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stats import skew, kurtosis


def dataframe(file_name, countries, years):
    df = pd.read_csv(file_name, skiprows=4)
    df.drop(["Country Code", "Indicator Code", "Indicator Name"], axis=1,
            inplace=True)
    df.dropna(how='any', thresh=100, axis=1, inplace=True)
    df.set_index(['Country Name'], inplace=True)
    df.index.rename("Country", inplace=True)
    #df.columns = pd.to_datetime(df.columns)
    df.columns.name = "Year"
    df_t = df.transpose()
    df_t.dropna(how='all', axis=1, inplace=True)
    df = df.loc[countries, years]
    df_t = df_t.loc[years, countries]
    return df, df_t


def stat(df):
    print(df.describe())
    print("\nSkewness:\n", skew(df))
    print("\nKurtosis:\n", kurtosis(df))
    return


def plotdf(df, name):
    ax = df.plot(subplots=True, figsize=(8, 9), fontsize=14)
    ax[0].set_title(name, fontsize=20, fontweight='bold')
    ax[-1].set_xlabel(str(df.index.name), fontsize=20)
    for i in range(0, len(ax)):
        ax[i].legend(fontsize=11.5)
    plt.tight_layout()
    plt.show()


countries = ["Belgium", "Denmark", "Finland", "India", "Japan", "South Africa",
             "United Kingdom", "United States"]
years = [str(i) for i in range(1994, 2015)]

df, df_t = dataframe("electricity from oil,gas,coal.csv", countries, years)
co, co_t = dataframe("co2 emission per capita.csv", countries, years)

stat(df_t)
stat(co_t)

plotdf(df_t, "Electicity Produced From oil, gas, coal (% of total)")

plotdf(co_t, "CO2 Emmission per capita")

years = [str(i) for i in range(1994, 2015, 5)]

nu, nu_t = dataframe("electricity from nuclear.csv", countries, years)

stat(nu_t)

nu.plot.bar(rot=35)
plt.show()

rn, rn_t = dataframe("Electricity from renewable ex hydro.csv",
                     countries, years)
hy, hy_t = dataframe("Electricity from hydro.csv", countries, years)

stat(rn_t.add(hy_t))

rn.add(hy).plot.bar(rot=35)
plt.show()
