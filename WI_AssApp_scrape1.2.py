# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:31:17 2020

@author: Kristen Swedberg
"""

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from time import sleep

###############################################################################
#                                DEFINE FUNCTIONS
###############################################################################

def print_url(url):
    """Keeps a record of all url's accessed, by print to csv."""

    with open(r'C:/LAGOS_Meta/WI/WI_Scraper/assapp_urls_accessed.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url])

    return


def write_error(url, error):
    """ Writes errors to error csv based on url and recorded error type. """

    with open(r'C:/LAGOS_Meta/WI/WI_Scraper/assapp_errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url, error])

    return

def get_building(tables):
    """ 
    Get building information if listed.
    
    If there is a building, the data is stored in btags in table 4.
    If the first btag says sale data, then there is no building.
    The buiding data will be updated with 'na' values.
    If there is a building the data will be stored. The title and blank elements are removed.
    Returns a 0-1 indicator for if there is a building. This value is used by get_sales.
    
    """
    
    build_text = []
    build_elems = tables[4].find_all('b')
    if build_elems[0].text == 'Sale Data':
        data['building'] = (['na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na',
                            'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na'])
        build_count = 0
    else:
        [build_text.append(build.text) for build in build_elems]
        data['building'] = build_text.copy()
        del data['building'][12:14]
        del data['building'][0:3]
        build_count = 1
    
    return build_count

def get_sales(tables, build_count):
    """
    Get sales info from table.
    
    Cannot get all sales info from btags, because data stored as td.
    Sales only stored in table 5 if there is a building.
    If there is not table it is stored in table 4.
    Tries to extract sales from correcct table. If exception, no sales. 
    If there are sales, a data and price will be listed for each sale.
    
    """
    if build_count == 1:
        sale_elems = tables[5]
    else:
        sale_elems = tables[4]

    try:
        sale_text = sale_elems.text.split()
        del sale_text[0:5]
        sale_count = int(len(sale_text)/2)
        data['sales'] = sale_text
    except:
        sale_count = 0   
    if data['sales'][0] == 'No':
        sale_count = 0
    
    return sale_count

def index_sales(sale_count):
    """
    Index sales and write to sales dictionary.
    
    Set the length of the index to the number of sales.
    The initial sale data and price values are in data['sales'][0] and [1] respectively.
    Assign a key name to each sale based on the index.
    Write a list of date and price for each sale to sale dictionary.
    
    """
    data['index'] = list(range(sale_count))
    
    date = 0        
    price = 1
    
    for i in data['index']:
        sales['sale_' + str(i)] = [data['sales'][date], data['sales'][price]]
        date += 2
        price += 2

def get_overview(tables):
    """ get overview data from table table 1. """
    
    over_text = []
    over_elems = tables[0].find_all('b')
    [over_text.append(over.text) for over in over_elems]
    data['overview'] = over_text[1:]

def get_general(tables):
    """ get overview data from table table 1. """
    
    gen_text = []
    gen_elems = tables[2].find_all('b')
    [gen_text.append(gen.text) for gen in gen_elems]
    data['general'] = gen_text[1:]


def get_trtags(content):
    """ Access all elements stored in tr tags. """
    
    tr_text = []
    tr_elems = content.find_all('tr')
    for tr in tr_elems:
        tr_text.append(tr.text.split())
    
    return tr_text


def get_land(content):
    """
    Get land information from tr_text    
    
    Land information is hidden when parsing tables, because it's tr tag '== $0' in html.
    Using selenium or scrapy could have accessed these elements directly.
    First get all tr tags, where the first land element is stored in tr tag 163. 
    Split the text in this field gives the property type, size, and units. 
    Test length of land to set units, beccause sq. ft. is parsed into two seperate fields.
    Input urls are residential only, so there should not be multiple types.
    When cleaning will test to ensure residential and that the acres/sq. ft. matches 
    the state level parcel information.
      
    """
    
    tr_text = get_trtags(content)
    try:
        land = tr_text[163]
        if len(land) == 2:
            unit = 'acres'
        else:
            unit = 'sq. ft.'
        data['land'] = [land[0], land[1], unit]
    except:
        land = tr_text[161]
        if len(land) == 2:
            unit = 'acres'
        else:
            unit = 'sq. ft.'
        data['land'] = [land[0], land[1], unit]
        
def row_data(url, sale_count):
    """ 
    Write all the information from data dictionary into single row for export.
    
    Row is extended, when adding a list.
    Row is appended, when adding a single value (or else it will turn the string into list).
    Row dictionary will be printed line by line.
    
    """

    for i in data['index']:
        row['row_' + str(i)] = [url]
        row['row_' + str(i)].extend(sales['sale_' + str(i)])
        row['row_' + str(i)].append(sale_count)
        row['row_' + str(i)].extend(data['overview'])
        row['row_' + str(i)].append(data['legal'])
        row['row_' + str(i)].extend(data['general'])
        row['row_' + str(i)].extend(data['land'])
        row['row_' + str(i)].extend(data['building'])
        

def write_row():
    """ Writes rows to csv. """

    with open(r'C:/LAGOS_Meta/WI/WI_Scraper/assapp_scraped_data1.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        [writer.writerow(row['row_' + str(i)]) for i in data['index']]

    return


###############################################################################
#                                MAIN CODE BLOCK
###############################################################################

#import urls
df = pd.read_csv(r'C:/LAGOS_Meta/WI/WI_Scraper/assapp_urls.csv')
urls = df['url']

#running through loop because small site i.e. need to scrape slowly
for url in urls:
    
    #sleep for 5 seconds in between urls to not overload server
    sleep(5)
    
    #initialize dictionary to store  data, sales, and row information
    data = {}
    sales = {}
    row = {}
    
    #get url and download content. if exception, sleep and try again
    #if second exception, record url error
    #continue means move to next url rather than finishing loop
    try:
        response = requests.get(url)
        content = BeautifulSoup(response.content, "html.parser")
        print_url(url)
    except:
        sleep(5)
        try:
            response = requests.get(url)
            content = BeautifulSoup(response.content, "html.parser")
            print_url(url)  
        except:
            error = 'url error'
            write_error(url, error)
            continue
    
    #if there is an internal servor error (bad url), len(tables) will be 0        
    tables = content.find_all('table', attrs={'cellpadding':'0', 'cellspacing':'2', 
                                      'border':'0', 'width':'100%'}) 
    if len(tables) == 0:
        error = 'url error'
        write_error(url, error)
        continue

    #record building and sale counts. if except, record count error
    try:
        building_count = get_building(tables)
        sale_count = get_sales(tables, building_count)
    except:
        error = 'count error'
        write_error(url, error)
        continue
    
    #if there are sales, continue collecting data. if exception, record data or write error
    if sale_count > 0:
        try:
            index_sales(sale_count)
            get_overview(tables)
            #legal info  stored in table 1 within 1 td tag
            data['legal'] = tables[1].find('td', attrs={'colspan':'3'}).text       
            get_general(tables)
            get_land(content)
        except:
            error = 'data error'
            write_error(url, error)
            continue
        try:
            row_data(url, sale_count)
            write_row()
        except:
            error = 'write error'
            write_error(url, error)
            continue
               