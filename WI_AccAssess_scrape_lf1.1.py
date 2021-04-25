# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 21:41:32 2020

@author: swedkm
"""

#for this one I am going to write all the intiial details to a single csv like ny lf

from selenium import webdriver
import pandas as pd
import csv
from multiprocessing import Pool
from time import sleep

def access_url(url):
    """ """
    try:
        driver.get(url)
        a = 'success'
    except:
        sleep(5)
        try:
            driver.get(url)
        except:
            a = 'error'
            access_error(url)

    return a

def print_url(url):
    """Keeps a record of all url's accessed, by print to csv."""

    with open(r'E:\WI_Results\url_accessed.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url])

    return


def access_error(url):
    """
    Writes access error to errors spreadsheet.

    """

    with open(r'E:\WI_Results\errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url, 'access error'])

    return

def read_error(url):
    """
    Writes access error to errors spreadsheet.

    """

    with open(r'E:\WI_Results\errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url, 'read error'])

    return

def write_error(url):
    """
    Writes access error to errors spreadsheet.

    """

    with open(r'E:\WI_Scraper\errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        writer.writerow([url, 'write error'])

    return

def div_data():
    """ """
    divs = driver.find_elements_by_xpath('/html/body/div/div')

    return divs

def single_split(divs):
    """ """

    for i in single_split_list:
        vals = divs[i].text.splitlines()
        try:
            data['single'].append(vals[1])
        except:
            data['single'].append('')

    return

def land_split(divs):
    """ """

    for i in land_split_list:
        vals = divs[i].text.splitlines()
        try:
            data['single'].append(vals[2])
        except:
            data['single'].append('')

    return

def no_split(divs):
    """" """

    for i in no_split_list:
        data['single'].append(divs[i].text)

    return

def sales_split(divs):
    """ """

    s_date = divs[85].text.splitlines()
    s_price = divs[86].text.splitlines()
    s_type = divs[87].text.splitlines()

    count = list(range(len(s_date)))
    del count[0]

    try:
        for i in count:
            elems = [s_date[i], s_price[i], s_type[i]]
            data['sales']['sale_' + str(i)] = [elem for elem in elems]
            data['index'].append(i)
    except:
        data['sales']['sale_1'] = ['na','na','na']
        data['index'].append(1)
    return

def row_data(url):
    """ """

    for i in data['index']:
        row['row_' + str(i)] = [url]
        row['row_' + str(i)].extend(data['single'])
        row['row_' + str(i)].extend(data['sales']['sale_' + str(i)])

    return

def write_rows():
    """

    """

    with open(r'E:\WI_Results\scraped_info_lf.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        [writer.writerow(row['row_' + str(i)]) for i in data['index']]

    return

def check_valid():
    """ """
    a = "true"

    try:
        if data['single'][0] == '':
            a = "false"
        if data['sales']['sale_1'][0] == 'na':
            a = "false"
    except:
        a = "false"

    return a

def scrape_data(url):
    """ """

    access_url(url)
    print_url(url)

    try:
        divs = div_data()
        single_split(divs)
        land_split(divs)
        no_split(divs)
        sales_split(divs)
        row_data(url)
    except:
        read_error(url)
        data['single'] = ['']

    a = check_valid()

    if a == "true":
        try:
            write_rows()
        except:
            write_error(url)

    return


#set path and open chromedrive
PATH = r'C:\Webdrivers\bin\chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH)

single_split_list = [4,5,6,8,9,10,12,14,64]
land_split_list = [91,92,93,94,95,96]
no_split_list = [18,20,25,28,30,33,35,38,40,43,45,48,50,53,55,58,60,99,101,103]

urls = pd.read_csv('E:\WI_Results\lf_urls.csv')

data = {}
data['single'] = []
data['index'] = []
data['sales'] = {}

row = {}

for url in urls['url']:
    data = {}
    data['single'] = []
    data['index'] = []
    data['sales'] = {}

    row = {}

    access_url(url)
    print_url(url)

    try:
        divs = div_data()
        single_split(divs)
        land_split(divs)
        no_split(divs)
        sales_split(divs)
        row_data(url)
    except:
        read_error(url)
        data['single'] = ['']

    a = check_valid()

    if a == "true":
        try:
            write_rows()
        except:
            write_error(url)