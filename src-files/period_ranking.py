"""
filename: period_ranking.py
author: Nick Creeley, nc8004@rit.edu
date: 11/7/2022
description: Computes rankings of a states or zip codes,
for a given year and given quarter.  

"""
from index_tools import *


def quarter_data(data,year,qtr):
    """
    Loops through data and populates (sorted) list with region/HPI tuples, 
    that have matching year and qtr to parameters.
    region/HPI tuples. 
    :param data: dicitonary mapping state region to list of QuarterHPI objects
    :param year: (int) year being queried 
    :param qtr: (int) quarter being queried
    :returns: sorted list of (region, HPI) tuples from high HPI to low HPI 
    """
    result = []
    for key in data:
        hpi_objects = data[key]
        for hpi_object in hpi_objects:
            if hpi_object.year == year and hpi_object.qtr == qtr:
                result.append((key,hpi_object.idx))
    result.sort(key=sortIndex,reverse=True)
    return result

def annual_data(data,year):
    """
    Loops through data and populates (sorted) list with region/HPI tuples, 
    that have matching year to parameter.
    region/HPI tuples. 
    :param data: dicitonary mapping region to list of AnnualHPI objects
    :param year: (int) year being queried 
    :returns: sorted list of (region, HPI) tuples from high HPI to low HPI 
    """
    result = []
    for key in data:
        annual_list = data[key]
        for annual_hpi in annual_list:
            if annual_hpi.year == year:
                result.append((key,annual_hpi.idx))
    result.sort(key=sortIndex,reverse=True)
    return result


def main():
    """
    Prompts user for file to process and year,
    processes file accordingly to if it is a state or ZIP file and what year was input,
    prints out rankings of annual HPI for that year.  
    :return: None
    """
    input_data = input("Enter region-based house price index filename: ")
    input_data = "data/" + input_data
    if "state" in input_data:
        data = read_state_house_price_data(input_data)
        year = int(input("Enter year of interest for house prices: "))
        annual = annualize(data)
        sorted_data = annual_data(annual,year)
        print_ranking(sorted_data,f"{year} Annual Ranking")

    else:
        year = int(input("Enter year of interest for house prices: "))
        data = read_zip_house_price_data(input_data)
        sorted_data = annual_data(data,year)
        print_ranking(sorted_data,f"{year} Annual Ranking")
    

# main’s code body here...
if __name__ == "__main__":
    main()