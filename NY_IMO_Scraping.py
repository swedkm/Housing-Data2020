# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:24:22 2020

@author: swedkm
"""

from selenium import webdriver
import pandas as pd
import csv
from multiprocessing import Pool
from time import sleep

# =============================================================================
# DEFINE FUNCTIONS
# not including owner data or improvements data.
# just getting minimum data for meta-analysis
# =============================================================================

def access(driver):
    """
    Gain access to a specific URL completeing neccessary data on municipality index site.

    This function is neccessary when visiting a municipality for first time or cookies timeout.
    First the browser will click the button "Click Here for Public Access".
    Next it will try to click the checkbox for "I agree" when rerouted to a disclaimer site.
    After this function is complete, the driver will be rerouted to the input URL.

    """

    driver.find_element_by_id("btnPublicAccess").click()
    try:
        driver.find_element_by_id("chkAgree").click()
        driver.find_element_by_id("btnSubmit").click()
    except:
        pass

    return

def write_row(file, row):
    """
    Writes a row in csv.

    Input file to export to.
    Input row as a list.
    Returns 1 when executed.

    """

    with open (file, 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow(row)

    return 1

def get_property_data(url, driver):
    """
    Read property data and write row to csv

    Initialize property data list with url for merging later.
    The data in span tags includes the property information and the inventory.
    The ids are listed in the SPAN_IDs dataframe with the headers ids.

    """

    property_data = [url]

    for span in SPAN_IDS['ids']:
        property_data.append(driver.find_element_by_id(span).text)

    return property_data

def get_sales_data(url, driver):
    """
    Input sales data into sales dictionary.

    The data for each sale will be stored in a seperate list.
    Each sale will be indexed by i.
    First find all the sales. Remove [0] because it stores the table headers.
    Next assign elements of each sale to its own list. Remove [9] because it is blank.
    Return sales dictionary. If no sales, return 'False' string.

    """
    sales_data = {}
    sales_table = driver.find_elements_by_xpath('/html/body/form/div[3]/div[6]/table/tbody/tr')
    i = 1
    try:
        del sales_table[0]
        for sale in sales_table:
            elems = sale.find_elements_by_tag_name('td')
            del elems[9]
            sales_data['sale_' + str(i)] = [elem.text for elem in elems]
            sales_data['sale_' + str(i)].append(url)
            i += 1
    except:
        sales_data = 'False'

    return sales_data



def scrape_data(swis):
    """
    Main function each pool will execute.

    Input a swis code referencing a list of urls.
    Iterate through each url, reading in reports page data and writing sales to csv.

    """

    #read in csv url
    df = pd.read_csv(INPUT_PATH + swis + 'urls.csv')

    #initialize write files
    property_file = PROPERTY_OUTPUT_PATH + swis + 'property_data.csv'
    sales_file = SALES_OUTPUT_PATH + swis + 'sales_data.csv'
    access_file = DEBUG_PATH + 'url_accessed1.0_' + swis + '.csv'
    errors_file = DEBUG_PATH + 'errors1.0_' + swis + '.csv'

    #initialize output csvs with headers
    pd.DataFrame(columns=list(PROPERTY_HEADERS)).to_csv(property_file, index=False)
    pd.DataFrame(columns=list(SALES_HEADERS)).to_csv(sales_file, index=False)
    pd.DataFrame(columns=['url']).to_csv(access_file, index=False)
    pd.DataFrame(columns=['url', 'error']).to_csv(errors_file, index=False)

    #open chromedriver window
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    for url in df['url']:

        #write url to accessed file. If file is open, error is triggered and console stops.
        write_row(access_file, [url])

        #try to go to url. skip to next url if it cannot be accessed.
        try:
            driver.get(url)
        except:
            sleep(2)
            try:
                driver.get(url)
            except:
                write_row(errors_file, [url, 'url error'])
            continue

        #try to get public access to site. if button not available access already granted.
        try:
            access(driver)
        except:
            pass

        #collect property data and write to csv
        try:
            property_data = get_property_data(url, driver)
            write_row(property_file, property_data)
        except:
            write_row(errors_file, [url, 'property error'])

        #collect sales data and write to csv
        try:
            sales_data = get_sales_data(url, driver)
            if sales_data != 'False':
                for sale in sales_data:
                    write_row(sales_file, sales_data[sale])
        except:
            write_row(errors_file, [url, 'sales error'])

    return swis
# =============================================================================
# MAIN CODE BLOCK
# =============================================================================
#set global paths
INPUT_PATH = r'C:/LAGOS_Meta/Initial_Cleaning_GIS/NY/NY_Scraper2.0/URLs/'
PROPERTY_OUTPUT_PATH = r'C:/LAGOS_Meta/Initial_Cleaning_GIS/NY/NY_Scraper2.0/Output/Property_Data/'
SALES_OUTPUT_PATH = r'C:/LAGOS_Meta/Initial_Cleaning_GIS/NY/NY_Scraper2.0/Output/Sales_Data/'
DEBUG_PATH = r'C:/LAGOS_Meta/Initial_Cleaning_GIS/NY/NY_Scraper2.0/Debug/'
DRIVER_PATH = r'C:\Webdrivers\bin\chromedriver.exe'

# import list of SWIS to input and headers for output data
SWIS_LIST = pd.read_csv(INPUT_PATH + 'swis_list.csv')
PROPERTY_HEADERS = pd.read_csv(INPUT_PATH + 'scraped_data_property_headers.csv')
SALES_HEADERS = pd.read_csv(INPUT_PATH + 'scraped_data_sales_headers.csv')
SPAN_IDS = pd.read_csv(INPUT_PATH + 'span_ids.csv')

# input list of swis strings
SWIS = []
for swis in SWIS_LIST['SWIS']:
    SWIS.append(str(swis))

if __name__ == "__main__":
	# creating a pool object
	p = Pool(5)

	# map list to target function
	result = p.map(scrape_data, SWIS)