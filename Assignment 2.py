# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 00:25:50 2023

@author: aaron
"""

import pandas as pd
import matplotlib.pyplot as plt
from stats import skew, kurtosis


def make_df1(file_name, countries, years):
    """ Function to read a csv file in world bank format, clean and slice it.
    Returns the dataframe and transposed dataframe.
    Arguments:
        Name/file path of a csv file.
        A list of countries required.
        A list of years required.
    """
    # reading from csv
    df = pd.read_csv(file_name, skiprows=4)

    # dropping columns that are not needed
    df.drop(["Country Code", "Indicator Code", "Indicator Name"], axis=1,
            inplace=True)
    df.dropna(how='any', thresh=100, axis=1, inplace=True)
    # filling nan value with 0
    df.fillna(0)

    # setting index
    df.set_index(['Country Name'], inplace=True)
    # renaming
    df.index.rename("Country", inplace=True)
    df.columns.name = "Year"

    # transposing
    df_t = df.transpose()

    # droping columns with nan values
    df_t.dropna(how='all', axis=1, inplace=True)

    # slicing required rows and columns
    df = df.loc[countries, years]
    df_t = df_t.loc[years, countries]

    # returnig cleaned and sliced df and transposed df
    return df, df_t


def read_df2(fname):
    """ Function to read a csv file in world in data format, converts to
    percentage and reverses column order. Returns the dataframe.
    Arguments:
        Name/file path of a csv file.
    """
    # reading from csv
    df = pd.read_csv(fname)

    # selecting world data only from 1990
    df_wrld = df[(df['Entity'] == "World") & (df['Year'] >= 1990)]
    # dropping columns that are not needed
    df_wrld.drop(["Entity", "Code"], axis=1, inplace=True)
    # setting index
    df_wrld.set_index("Year", inplace=True)

    # coverting data to percentage
    df_wrld_percent = df_wrld.apply(lambda x: round((x/sum(x)*100), 2), axis=1)

    # using lambda functions to rename columns
    df_wrld_percent =\
        df_wrld_percent.rename(columns=lambda x: x.replace('Electricity from ',
                                                           ''))
    df_wrld_percent =\
        df_wrld_percent.rename(columns=lambda x: x.replace(' (TWh)', ''))
    df_wrld_percent = \
        df_wrld_percent.rename(columns=lambda x: x.replace(' (zero filled)',
                                                           ''))
    # renaming one more column
    df_wrld_percent =\
        df_wrld_percent.rename(columns={"Other renewables excluding bioenergy":
                                        "Other Renewables"})
    # capitalising column names
    df_wrld_percent.columns = df_wrld_percent.columns.str.capitalize()

    # reversing order of columns for better plot
    df_wrld_percent_reversed = df_wrld_percent.iloc[:, ::-1]

    # returning required df
    return df_wrld_percent_reversed


def stat_df(df):
    """ Function to give a statistic overview of a dataframe.
    Prints a dataframe that includes mean, std, min, 25%, 50%, 75%, max,
    skewness, and kurtosis of the given df.
    Arguments:
        A dataframe.
    """
    # using statistical tools
    des = df.describe()
    sk = skew(df)
    kurt = kurtosis(df)

    # coverting sk and kurt to dataframe to concatenate
    sk = pd.DataFrame([sk], columns=des.columns, index=["skewness"])
    kurt = pd.DataFrame([kurt], columns=des.columns, index=["kurtosis"])

    # concatenating them to one df for a better look
    stat = pd.concat([des, sk, kurt])

    # printing
    print(stat)
    return


def plot_df(df, kind, name):
    """ Function to create a plot.
    Arguments:
        A dataframe.
        A kind of plot required.
        Name of the plot.
    """
    # using if else for different kinds of plot
    if kind == "area":

        # plotting
        ax = df.plot.area(colormap='RdYlBu', figsize=(14, 9), fontsize=20)
        # setting title
        ax.set_title(name, fontsize=29, fontweight='bold')
        # setting xlabel
        ax.set_xlabel(str(df.index.name), fontsize=27)
        # customising legend
        plt.legend(fontsize=20, bbox_to_anchor=(1, 0.75))

    elif kind == "line":

        # styles for line plot
        styles = ['>-' for i in range(len(df.columns))]
        # plotting
        ax = df.plot(subplots=True, figsize=(8, 9), fontsize=18, style=styles,
                     sharex=True)
        # setting title
        ax[0].set_title(name, fontsize=20.5, fontweight='bold')
        # setting xlabel
        ax[-1].set_xlabel(str(df.index.name), fontsize=25)
        # customising legend for each subplot
        for i in range(0, len(ax)):
            ax[i].legend(fontsize=14)

    elif kind == "bar":

        # plotting
        ax = df.plot.bar(rot=40, figsize=(10, 9), fontsize=18, width=0.6,
                         edgecolor='black')
        # setting title
        ax.set_title(name, fontsize=22, fontweight='bold')
        # setting xlabel
        ax.set_xlabel(str(df.index.name), fontsize=28)
        # customising legend
        ax.legend(fontsize=23)

    else:
        print("Only 'area', 'line' or 'bar' plots available")

    # removing unwanted whitespaces
    plt.tight_layout()

    # svaing the plot
    plt.savefig((name + ".png"), dpi=500, bbox_inches="tight")

    plt.show()
    return


# making dataframe
source_df = read_df2("electricity-prod-source-stacked.csv")

# plotting
plot_df(source_df, "area",
        "Electricity Produced from each Source (% of total)")

# listing required countries and years
countries = ["Australia", "Denmark", "Brazil", "Japan", "France", "Bangladesh",
             "United Kingdom", "United States"]
years = [str(i) for i in range(1994, 2015)]

# making dataframes
ogc, ogc_t = make_df1("electricity from oil,gas,coal.csv", countries, years)
co, co_t = make_df1("co2 emission per capita.csv", countries, years)

# getting statistical overview
stat_df(ogc_t)
stat_df(co_t)

# ploting line plots
plot_df(ogc_t, "line", "Electicity Produced from Oil, Gas,Coal (% of total)")
plot_df(co_t, "line", "CO2 Emmission per capita")

# changing years for better bar graph
years = [str(i) for i in range(1994, 2015, 5)]

# making dataframe
nuclear, nuclear_t = make_df1("electricity from nuclear.csv", countries, years)

# getting statistical overview
stat_df(nuclear_t)

# plotting
plot_df(nuclear, "bar",
        "Electicity Produced from Nuclear Sources (% of total)")

# making dataframes
ex_hydro, ex_hydro_t = make_df1("Electricity from renewable ex hydro.csv",
                                countries, years)
hydro, hydro_t = make_df1("Electricity from hydro.csv", countries, years)

# adding to get df of all renewable sources
renewable = ex_hydro.add(hydro)
renewable_t = ex_hydro_t.add(hydro_t)

# getting statistical overview
stat_df(renewable_t)

# plotting
plot_df(renewable, "bar",
        "Electicity Produced from Renewable Sources (% of total)")
