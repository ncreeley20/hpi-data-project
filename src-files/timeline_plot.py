"""
filename: timeline_plot.py
author: Nick Creeley, nc8004@rit.edu
date: 11/7/2022
description: graphs changes in HPI values over time.

"""
import numpy.ma as ma
import matplotlib.pyplot as plt


from index_tools import * 


def build_plottable_array(xyears,regiondata):
    """
    Makes an array suitable for plotting with matplotlib
    :param xyears: list of years being evaluated
    :param regiondata: regional data being used
    :return: masked array of values
    """
    year_dict = {}
    value_list = []
    for year in xyears:
        year_dict[year] = 0
    for data in regiondata:
        for key in year_dict:
            if key == data.year:
                year_dict[key] += data.idx
    for value in year_dict.values():
        value_list.append(value)
    result = ma.array(value_list)
    for i in range(len(result)):
        if result[i] == 0:
            result[i] = ma.masked
    return result


def filter_years(data,year0,year1):
    """
    Filters a dictionary of AnnualHPI values within a range of years.
    :param data: dictionary mapping regions to list of AnnualHPI values
    :param year0: beginning year
    :param year1: ending year
    :precondition: year0 <= year1
    :return: dictionary mapping regions to lists of HPI values that are within the year range. 

    """
    result = {}
    for key in data:
        annual_list = data[key]
        for annualHPI in annual_list:
            if  year0 <= annualHPI.year <= year1:
                if key in result:
                    result[key].append(annualHPI)
                else:
                    result[key] = [annualHPI] 
    return result

def plot_HPI(data,regionList):
    """
    Plots data for regions given in a region list
    :param data: dictionary mapping a state or zipcode to AnnualHPI objects
    :param regionList: list of string keys
    :return: None
    """
    start_years = []
    end_years = []
    for region in regionList:
        regiondata = data[region]
        startyear = regiondata[0].year
        endyear = regiondata[-1].year
        start_years.append(startyear)
        end_years.append(endyear)
        x_values = ma.array([i for i in range(startyear,endyear)])
        y_values = build_plottable_array(x_values,regiondata)
        plt.plot(x_values,y_values,marker='.',label = f"{region}")
    plt.legend()
    real_start_year = min(start_years)
    real_end_year = max(end_years)
    plt.title(f"Home Price Indices: {real_start_year}-{real_end_year}")
    plt.show()

def plot_whiskers(data,regionList):
    plot_data = []
    names = []
    for region in regionList:
        regiondata = data[region]
        startyear = regiondata[0].year
        endyear = regiondata[-1].year
        values = build_plottable_array([i for i in range(startyear,endyear)],regiondata)
        plot_data.append(values)
        names.append(region)
    xticks_helper = [i for i in range(1,len(names) +1)]
    ax = plt.subplot()
    ax.boxplot(plot_data,showmeans=True)
    plt.xticks(xticks_helper,names)
    plt.title("Home Price Index Comparison.Median is a line. Mean is a triangle.")
    plt.show()
        

def main():
    """
    Asks user for file to plot, start year, end year and regions of interest.
    Plots data for given year list. 

    """
    regionList = []
    user_file = input("Enter house price index filename: ")
    user_file = "data/" + user_file
    startyear = int(input("Enter start year of range to plot: "))
    endyear = int(input("Enter end year of range to plot: "))
    while True:
        region = input("Enter next region for plots (ENTER to stop): ")
        if region == "":
            break
        else:
            regionList.append(region)
    if "state" in user_file:
        data = read_state_house_price_data(user_file)
        annual = annualize(data)
        annual = filter_years(annual,startyear,endyear)
        print("Close window when done viewing")
        plot_HPI(annual,regionList)
        plot_whiskers(annual,regionList)
    else:
        data = read_zip_house_price_data(user_file)
        annual = filter_years(data,startyear,endyear)
        print("Close window when done viewing")
        plot_HPI(annual,regionList)
        plot_whiskers(annual,regionList)
    

if __name__ == "__main__":
    main()