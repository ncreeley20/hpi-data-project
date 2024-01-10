"""
filename: trending.py
author: Nick Creeley, nc8004@rit.edu
date: 11/7/2022
description: computes the top and bottom trending regions,
based on growth during a time period.

"""

from index_tools import *


def cagr(idxlist,periods):
    """
    Calculates the compound annual growth rate, CAGR for a period.
    :param idxlist: 2 item list of HPI0 and HPI1, HPI0 is earlier period index 
    :param periods: (int) number of years between two HPI values in list
    :return: float representing cagr expressed as percentage
    """
    return (((idxlist[1]/idxlist[0])**(1/periods))-1)*100

def calculate_trends(data,year0,year1):
    """
    Calculates cagr values for a data mapping region to AnnualHPI and sorts it.
    :param data: dictionary from region to list of AnnualHPI
    :param year0: (int) starting year of interest
    :param year1: (int) ending year of interest
    :preconditions: year1 > year0
    :return: list of (region,rate) tuples sorted in descending order by rate.
    """
    result = []
    for key in data:
        annual_list = data[key]
        idxlist = []
        for annualHPI in annual_list:
            if annualHPI.year == year0:
                idxlist.append(annualHPI.idx)
            elif annualHPI.year == year1:
                idxlist.append(annualHPI.idx)
        if len(idxlist) == 2:
            rate = cagr(idxlist,(year1-year0))
            result.append((key,rate))
    result.sort(key = sortIndex,reverse=True)
    return result


def main():
    """
    Prompts user for file to read, starting year and ending year,
    prints out a top 10/bottom 10 list of compound annual growth rate for the timespan.
    :return: Nonetype

    """
    file_input = input("Enter house price index filename: ")
    year0 = int(input("Enter start year of interest: "))
    year1 = int(input("Enter ending year of interest: "))
    file_input = "data/" + file_input
    if "state" in file_input:
        data = read_state_house_price_data(file_input)
        data = annualize(data)
        trending = calculate_trends(data,year0,year1)
        print_ranking(trending,f"{year0}-{year1} Compound Annual Growth Rate")
    else:
        data = read_zip_house_price_data(file_input)
        trending = calculate_trends(data,year0,year1)
        print_ranking(trending,f"{year0}-{year1} Compound Annual Growth Rate")

# main’s code body here...
if __name__ == "__main__":
    main()
