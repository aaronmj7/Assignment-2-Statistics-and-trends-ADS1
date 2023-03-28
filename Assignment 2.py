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
    df.columns.name = "Years"
    df = df.loc[countries, years]
    df_t = df.transpose()
    return df, df_t


countries = [""]
