# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:06:40 2020

@author: swedkm
"""

from selenium import webdriver
import pandas as pd
from time import sleep
import csv
import random

# ===================================================================================
#                                   DEFINE FUNCTIONS
# ===================================================================================

def sales_info(url, county):
    """
    Tests to see if there is a valid sale. If yes, sales stored in data dictionary.

    Tries to find the owner and purchase fields. If not present, no sale information recorded.
    Parses the date field to find sales in valid timeframe. If error, write entire field to error log.
    Parses the price field to find invalid sales of $0. If error, write entire field to error log.
    Returns 0 for valid sale or 1 for no sale or invalid sale.

    """

    try:
        date = driver.find_element_by_xpath("//*[contains(text(), 'Owner Since:')]").text.split(':')
        price = driver.find_element_by_xpath("//*[contains(text(), 'Purchase Price:')]").text.split(':')

        try:
            d = date[1].split('/')
            year = int(d[2])
            month = int(d[0])

            if year < 2001:
                s = 1
            elif year > 2015:
                s = 1
            else:
                s = 0
        except:
            error = 'date error: ' + str(date)
            write_error(url, error, county)
            s = 1

        try:
            p1 = price[1].split('$')
            p2 = p1[1].split(',')
            p_parts = []
            for p in p2:
                p_part = p.split('.')
                p_parts.extend(p_part[0])
            p_numeric = int(''.join(p_parts))

            if p_numeric == 0:
                s = 1
            else:
                s = 0
        except:
            error = 'price error: ' + str(price)
            write_error(url, error, county)
            s = 1

        if s == 0:
            data['sales'] = [date[1], year, month, price[1], p_numeric]

    except:
        s = 1

    return s


def address_info():
    """
    Extracts valid address information and exports to dictionary.

    The address is the first of the h-widget classes.
    Returns 0 for valid address and 1 if there is no street address.
    Does not need try and except, because all pages have an address. Exception will raise url error.

    """

    full = driver.find_element_by_class_name('h-widget').text
    f_parts = full.split(',')
    if f_parts[0] == '':
        a = 1
    else:
        a = 0
        street = f_parts[0]
        data['address'] = [full, street]

    return a

def property_info(url, county):
    """
    Extract property details and export to dictionary.

    Initializes values for dictionary.
    Tries to update values with specific property details.
    If all values updated, return 0.
    If error, update error log and return 1.

    """

    site = 'na'
    town = 'na'
    lval = 'na'
    bval = 'na'
    tval = 'na'

    try:
        site = driver.find_element_by_xpath("//*[contains(text(), 'Site:')]").text.split(':')[1]
        town = driver.find_element_by_xpath("//*[contains(text(), 'Town:')]").text.split(':')[1]
        lval = driver.find_element_by_xpath("//*[contains(text(), 'Land Value:')]").text.split(':')[1]
        bval = driver.find_element_by_xpath("//*[contains(text(), 'Building Value:')]").text.split(':')[1]
        tval = driver.find_element_by_xpath("//*[contains(text(), 'Total Real Value:')]").text.split(':')[1]
        p = 0
    except:
        error = 'property error: ' + str(data['property'])
        write_error(url, error, county)
        p = 1

    data['property'] = [site, town, lval, bval, tval]

    return p

def land_info(url, county):
    """
    Extract property details and export to dictionary.

    Tries parsing total lot size. If error, update error log and return 1.
    Tries parsing individual lots. Reads the name, size, and units for each lots and stores in 3 lists.
    Updates data dictionary with total acreage/units, information for 1st 3 lots, and the total number of lots.
    If successful return 0. If error, update error log and return 2.

    """

    try:
        table = driver.find_element_by_id('cama-land-details')
        summary = table.find_element_by_tag_name('tfoot')
        lsize = summary.find_elements_by_tag_name('th')[1].text.split()
        tsize = lsize[0]
        tunits = lsize[1]

        try:
            lots = table.find_elements_by_xpath("//*[contains(text(), 'Primary Lot')]")
            data['lots'] = []
            for lot in lots:
                l = lot.text.split(':')[1]
                data['lots'].append(l)

            sizes = table.find_elements_by_xpath("//*[contains(text(), 'Primary Lot')]/following-sibling::td")
            data['sizes'] = []
            data['units'] = []
            for size in sizes:
                s_u = size.text.split()
                s = s_u[0]
                u = s_u[1]
                data['sizes'].append(s)
                data['units'].append(u)

            lot_count = len(lots)
            if lot_count == 1:
                data['land'] = ([tsize, tunits, lot_count, data['lots'][0], data['sizes'][0],
                                data['units'][0], 'na', 'na', 'na', 'na', 'na', 'na'])
            elif lot_count == 2:
                data['land'] = ([tsize, tunits, lot_count, data['lots'][0], data['sizes'][0],
                                data['units'][0], data['lots'][1], data['sizes'][1], data['units'][1],
                                'na', 'na', 'na'])
            else:
                data['land'] = ([tsize, tunits, lot_count, data['lots'][0], data['sizes'][0],
                                data['units'][0], data['lots'][1], data['sizes'][1], data['units'][1],
                                data['lots'][2], data['sizes'][2], data['units'][2]])
            l = 0
        except:
            data['land'] = [tsize, tunits, 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na']
            error = 'land partials error'
            write_error(url, error, county)
            l = 2

    except:
        error = 'land totals error'
        write_error(url, error, county)
        l = 1

    return l

def building_info(url, county):
    """
    Extract building details and export to dictionary.

    Initialize building count at 0
    Locate building rows through selectors. If no building rows, return 2.
    good resource for css selectors: https://saucelabs.com/resources/articles/selenium-tips-css-selectors
    If building elements, report number of buildings and store building type, area, value, and year for the first 10.
    """

    build_count = 0
    try:
        buildings = driver.find_elements_by_xpath("//div[@id='cama-primary-building-data']//tbody//tr[@role='row']")
        build_count = len(buildings)
        if build_count == 0:
            b = 2
        else:
            data['build_init'] = [build_count]
            build_elems = {}
            i = 1
            for building in buildings:
                elems = building.find_elements_by_tag_name('td')
                build_elems['row_' + str(i)] = [elem.text for elem in elems]
                data['build_init'].append(build_elems['row_' + str(i)][0])
                data['build_init'].append(build_elems['row_' + str(i)][1])
                data['build_init'].append(build_elems['row_' + str(i)][6])
                data['build_init'].append(build_elems['row_' + str(i)][8])
                i += 1

            if build_count > 10:
                data['building'] = data['build_init'][:41]
            else:
                na_build = 10 - build_count
                na_count = list(range(4*na_build))
                data['building'] = data['build_init'].copy()
                [data['building'].append('na') for na in na_count]
            b = 0
    except:
        error = 'building error: ' + str(build_count)
        write_error(url, error, county)
        b = 1

    return b

def data_concat(url):
    """Concactenate the elements a single list."""

    data['write'] = [url]
    data['write'].extend(data['address'])
    data['write'].extend(data['sales'])
    data['write'].extend(data['land'])
    data['write'].extend(data['property'])
    data['write'].extend(data['building'])

    return

def write_data(county):
    """
    Write each list from the row dictionary into a row in the output csv.

    Set to append mode. New rows appended for each url.

    """

    with open(r'C:/LAGOS_Meta/ME/Housing Data/Process/jeo/' + county + '_scraped_info_lf.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow(data['write'])

    return

def write_error(url, error, county):
    """
    Write error to error csv.

    """

    with open(r'C:/LAGOS_Meta/ME/Housing Data/Process/jeo/' + county + '_errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url, error])

    return

def write_url(url, county):
    """
    Update log of all urls visited.

    """

    with open(r'C:/LAGOS_Meta/ME/Housing Data/Process/jeo/' + county + '_urls_visited.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url])

    return


# ===================================================================================
#                                   MAIN CODE BLOCK
# ===================================================================================

# Set PATH for Chromedriver test window.
PATH = r'C:\Webdrivers\bin\chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH)

#import urls dataframe
df = pd.read_csv(r'C:/LAGOS_Meta/ME/Housing Data/Process/jeo/url_parcels2.csv')

#consider moving this to pool process but keep sleep in
#storing url county inforamtion in one elements that can be split into county and url
for index, row in df.iterrows():
    #read information from dataframe
    url = row['url']
    county = row['COUNTY']

    #initialize data dictionary
    data = {}
    data['address'] = []
    data['sales'] = []
    data['land'] = []
    data['property'] = []
    data['building'] = []
    data['write'] = []

    try:
        #go to url and write to urls_visited .csv to track progress.
        #if cannot access move to next url.
        driver.get(url)
        write_url(url, county)

        #sleep after get, because page slow to load
        sleep(random.randint(10,20))

        #test if parcel has a valid address. if not move to next url.
        a = address_info()
        if a == 1:
            continue
        else:
            #test if parcel has valid sales. if not move to next url.
            s = sales_info(url, county)
            if s == 1:
                continue
            else:
                #collect land information. If error code 1, move to next url
                l = land_info(url, county)
                if l == 1:
                    continue
                #collect property and building info. If errors, results still reported
                else:
                    p = property_info(url, county)
                    b = building_info(url, county)
                    data_concat(url)
                    write_data(county)
    except:
        error = 'url error'
        write_error(url, error, county)
