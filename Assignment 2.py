# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 00:25:50 2023

@author: aaron
"""

import pandas as pd
import matplotlib.pyplot as plt
from stats import skew, kurtosis


def dataframe(file_name, countries, years):
    """Function to read a csv file in world bank format, clean and slice it.
    Returns the dataframe and transposed dataframe. Arguments:
        Name/file path of a csv file.
        A list of countries required.
        A list of years required.
    """
    df = pd.read_csv(file_name, skiprows=4)
    df.drop(["Country Code", "Indicator Code", "Indicator Name"], axis=1,
            inplace=True)
    df.dropna(how='any', thresh=100, axis=1, inplace=True)
    df.set_index(['Country Name'], inplace=True)
    df.index.rename("Country", inplace=True)
    df.columns.name = "Year"
    df_t = df.transpose()
    df_t.dropna(how='all', axis=1, inplace=True)
    df = df.loc[countries, years]
    df_t = df_t.loc[years, countries]
    return df, df_t


def stat(df):
    """Function to give a statistic overview of a dataframe.
    Includes mean, std, min, 25%, 50%, 75%, max, skewness, kurtosis. Arguments:
        A dataframe.
    """
    des = df.describe()
    sk = skew(df)
    kurt = kurtosis(df)
    sk = pd.DataFrame([sk], columns=des.columns, index=["skewness"])
    kurt = pd.DataFrame([kurt], columns=des.columns, index=["kurtosis"])
    stat = pd.concat([des, sk, kurt])
    print(stat)
    return


def plotdf(df, kind, name):
    """Function to create a plot. Arguments:
    A dataframe.
    A kind of plot required.
    Name of the plot.
    """
    if kind == "line":
        ax = df.plot(subplots=True, figsize=(8, 9), fontsize=18, grid=True)
        ax[0].set_title(name, fontsize=20.5, fontweight='bold')
        ax[-1].set_xlabel(str(df.index.name), fontsize=25)
        for i in range(0, len(ax)):
            ax[i].legend(fontsize=14)
    elif kind == "bar":
        ax = df.plot.bar(rot=40, figsize=(10, 9), fontsize=18, width=0.6,
                         edgecolor='black')
        ax.set_title(name, fontsize=22, fontweight='bold')
        ax.set_xlabel(str(df.index.name), fontsize=28)
        ax.legend(fontsize=23)
    else:
        print("Only 'line' or 'bar' plots available")
    plt.tight_layout()
    plt.savefig((name + ".png"), dpi=500)
    plt.show()
    return


countries = ["Belgium", "Denmark", "Finland", "India", "Japan",
             "United Kingdom", "United States"]
years = [str(i) for i in range(1994, 2015)]

df, df_t = dataframe("electricity from oil,gas,coal.csv", countries, years)
co, co_t = dataframe("co2 emission per capita.csv", countries, years)

stat(df_t)
stat(co_t)

plotdf(df_t, "line", "Electicity Produced from Oil, Gas,Coal (% of total)")

plotdf(co_t, "line", "CO2 Emmission per capita")

years = [str(i) for i in range(1994, 2015, 5)]

nu, nu_t = dataframe("electricity from nuclear.csv", countries, years)

stat(nu_t)

plotdf(nu, "bar", "Electicity Produced from Nuclear Sources (% of total)")

rn, rn_t = dataframe("Electricity from renewable ex hydro.csv",
                     countries, years)
hy, hy_t = dataframe("Electricity from hydro.csv", countries, years)

stat(rn_t.add(hy_t))

plotdf(rn.add(hy), "bar",
       "Electicity Produced from Renewable Sources (% of total)")
