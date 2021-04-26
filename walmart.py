# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:00:19 2020

@author: swedkm
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from multiprocessing import Pool
from time import sleep
import csv

def search_address(location):
    """Input the town into the search field """

    elem = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/form/div/div[3]/div/input[1]')
    elem.send_keys(location)
    elem.send_keys(Keys.RETURN)

    return

def get_directions():
    """
    Click the directions button and searches for nearest walmart.

    Sometimes your location is stored in the search field.
    Backspace until the field is empty before entering walmart.
    Click enter multiple times, to go past the "did you mean" box.

    """

    driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div[1]/div/button').click()
    sleep(2)
    elem = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div/div/input')
    delete = 'Your Location'
    for d in delete:
        elem.send_keys(Keys.BACKSPACE)
    elem.send_keys('Walmart')
    sleep(1)
    elem.send_keys(Keys.RETURN)
    sleep(1)
    elem.send_keys(Keys.RETURN)
    sleep(1)
    elem.send_keys(Keys.RETURN)

    return

def read_result(location):
    """
    Find the location of and distance to nearest store

    UPDATE FULL XPATH FOR DISTANCE BEFORE NEW RUNS

    """

    #location is embedded within input label attribute
    elem = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div/div/input')
    label = elem.get_attribute('aria-label')

    #remove "Starting point " from location
    loc = label[15:].split(',')

    #time and distance are text elements
    try:
        dist = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div[1]/div/div[1]/div[1]/div[2]/div').text.split()

    except:
        try:
            dist = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[2]/div').text.split()
        except:
            pass
    try:
        info = [location, loc[0], loc[1][1:], loc[2][1:], loc[3][4:], dist[0], dist[1]]
    except:
        info = [location, loc[0], '', loc[1][1:], loc[2][1:], dist[0], dist[1]]

    return info

def write_info(info):
    """ Append csv with info from each address search """

    with open(output_file_location, 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow(info)

    print(info)

    return

def write_address(location):
    """ Write each address searched """

    with open(tracker_file_location, 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([location])

    return

def write_error(error):
    """ Print error message to log """

    with open(error_file_location, 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow(error)

    return

def scrape_data(location):
    """ Scrapes data using predefined functions. """

    driver.get('https://www.google.com/maps')
    sleep(2)
    write_address(location)
    try:
        search_address(location)
    except:
        error = [location, 'search error']
        write_error(error)
    sleep(3)
    try:
        get_directions()
    except:
        error = [location, 'directions error']
        write_error(error)
    sleep(4)
    try:
        info = read_result(location)
        try:
            write_info(info)
        except:
            error = [location, 'write error']
            write_error(error)
    except:
        error = [location, 'read error']
        write_error(error)

    return


##################################################################################
# MAIN CODE BLOCK
##################################################################################
PATH = r'C:\Webdrivers\bin\chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH)
#rerun individually if there are only a few errors
#location = '42.77240344N 076.92476512W'
#locations = ['41.59658046N 074.70863931W', '42.46625399N 076.52550264W', '42.48662055N 077.56315050W', '42.71754764N 076.96451540W']
#for location in locations:
#    scrape_data(location)

#initialize file locations for each run
directory = r'C:/LAGOS_Meta/Aggregate_Hedonic/Clean_Data_Prep/MN/'
input_file_location = directory + 'walmart/ottertail_locations_clean1.2.csv'
input_field = 'DDLatLon'
output_file_location = directory + 'walmart_output1.0.1.csv'
error_file_location = directory + 'walmart/walmart_error1.0.1.csv'
tracker_file_location = directory + '/walmart/walmart_tracker1.0.1.csv'

#prior township not working in google maps
#recleaned and set to Ortonville, but some are located in Clinton.
#These were manually changed, see redo2.
#also lovgren's wood shore to lovegren woodshore
if __name__ == "__main__":

    input_file = pd.read_csv(input_file_location)
    location = input_file[input_field].tolist()

    p = Pool(4)
    result = p.map(scrape_data, location)
    p.terminate()
    p.join()