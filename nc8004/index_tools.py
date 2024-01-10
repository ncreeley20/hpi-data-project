"""
filename: index_tools.py
author: Nick Creeley, nc8004@rit.edu
date: 11/7/2022
description: Holds various functions for use in other modules.

"""

from dataclasses import dataclass

@dataclass 
class QuarterHPI:
    year: int
    qtr: int
    idx: float

@dataclass
class AnnualHPI:
    year: int
    idx: float

def sortIndex(val):
    """
    Helper function to help sort list of tuples,
    by index value using python built in sort() fcn.
    :param val: tuple being sorted
    :return: second value in tuple 
    """
    return val[1]

def read_state_house_price_data(filepath):
    """
    Reads state files, populates dictionary with data
    :param filepath: string, giving the name of a data file
    :return: dictionary populated with data
    """
    result = {}
    with open(filepath) as file:
        line = file.readline()
        if line[:5] == "state":
            pass
        else:
            line = line.strip().split()
            if line[3] == ".":
                print('data unavailable:')
                print(" ".join(line))
            else:
                year = int(line[1])
                qtr = int(line[2])
                idx = float(line[3])
                quarterhpi = QuarterHPI(year,qtr,idx)
                result[line[0]] = [quarterhpi]
        for line in file:
            line = line.strip().split()
            if line[3] == ".":
                print('data unavailable:')
                print(" ".join(line))
            else:
                year = int(line[1])
                qtr = int(line[2])
                idx = float(line[3])
                quarterhpi = QuarterHPI(year,qtr,idx)
                if line[0] in result:
                    result[line[0]].append(quarterhpi)
                else:
                    result[line[0]] = [quarterhpi]
    return result
          
def read_zip_house_price_data(filepath):
    """
    Reads zip file data, puts data in a dictionary
    :param filepath: string giving the path name of a ZIP5 data file
    :return: dictionary populated with data from file
    """
    result = {}
    count = 0
    uncounted = 0
    with open(filepath) as file:
        file.readline()
        for line in file:
            line = line.strip().split()
            if line[3] == '.':
                uncounted += 1
            else:
                count += 1
                year = int(line[1])
                idx = float(line[3])
                annualhpi = AnnualHPI(year,idx)
                if line[0] in result:
                    result[line[0]].append(annualhpi)
                else:
                    result[line[0]] = [annualhpi]
    print(f"count: {count} uncounted: {uncounted}")
    return result
    

def index_range(data,region):
    """
    Finds the largest and smallest indexes from a region.
    :param data: dictionary mapping regions to list of HPI objects
    :param region: (string) region name 
    :return: tuple of HPI objects that are low and high index values
    """
    data_list = data[region]
    min = data_list[0]
    max = data_list[0]
    for hpi in data_list:
        if hpi.idx < min.idx:
            min = hpi
        if hpi.idx > max.idx:
            max = hpi
    return (min,max)
       

def print_range(data,region):
    """
    Prints the low and high values of HPI for region.
    :param data: dictionary mapping regions to lists of HPI objects
    :param region: (string) region wanting to further explore
    :return: None
    """
    range = index_range(data,region)
    low = range[0]
    high = range[1]
    print(f"Region: {region}")
    try:
        test = low.qtr
        print(f"Low: year/quarter/index: {low.year} / {low.qtr} / {low.idx}")
        print(f"High: year/quarter/index: {high.year} / {high.qtr} / {high.idx}")
    except:
        print(f"Low: year/index: {low.year} / {low.idx}")
        print(f"High: year/index: {high.year} / {high.idx}")


def print_ranking(data,heading= "Ranking"):
    """
    Prints table of top ten and bottom of HPI values.
    :param data: already sorted list of tuples
    :return: None
    """
    if data[0][1] < data[-1][1]:
        data.reverse()
        print(heading)
        print("The Top 10:")
        number = 1
        for tuple in data[0:10]:
            print(f"{number} : {tuple} ")
            number += 1
        print("The Bottom 10:")
        number = len(data) - 9
        for tuple in data[-10:]:
            print(f"{number} : {tuple}")
            number += 1
    else:
        print(heading)
        print("The Top 10:")
        number = 1
        for tuple in data[0:10]:
            print(f"{number} : {tuple} ")
            number += 1
        print("The Bottom 10:")
        number = len(data) - 9
        for tuple in data[-10:]:
            print(f"{number} : {tuple}")
            number += 1


def annualize(data):
    """
    Computes AnnualHPI objects by averaging Quarter HPI indexes.
    :param data: dictionary mapping regions to lists of QuarterHPI objects
    :return: dictionary mapping regions to lists of AnnualHPI objects 
    """
    result = {}
    for key in data:
        result[key] = []
        data_list = data[key]
        year_dict = {}
        for object in data_list:
            if object.year in year_dict:
                year_dict[object.year].append(object.idx)
            else:
                year_dict[object.year] = [object.idx]
        for year in year_dict:
            idx_list = year_dict[year]
            idx_sum = sum(idx_list)/len(idx_list)
            annual_hpi = AnnualHPI(year,idx_sum)
            result[key].append(annual_hpi)
    return result

        
def main():
    """
    Prompts the user for data to process,
    checks if it is either state or ZIP file,
    processes and prints data accordingly.
    :return: None
    """
    input_data = input("Enter house price index file: ")
    input_data = "data/" + input_data
    if "state" in input_data:
        data = read_state_house_price_data(input_data)
        while True:
            input_region = input("Next region of interest (Hit ENTER to stop):" )
            if input_region == "":
                break
            else:
                print("=" * 30)
                print_range(data,input_region)
                annual_data = annualize(data)
                print_range(annual_data,input_region)
                print(f"Annualized Index Values for {input_region}: ")
                for object in annual_data[input_region]:
                    print(object)
                    
    else:
        data = read_zip_house_price_data(input_data)
        while True:
            input_region = input("Next region of interest (Hit ENTER to stop):" )
            if input_region == "":
                break
            else:
                print("=" * 30)
                print_range(data,input_region)
                print(f"Annualized Index Values for {input_region}: ")
                for object in data[input_region]:
                    print(object)
        

if __name__ == "__main__":
    main()

