# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 23:31:44 2020

@author: Kristen Swedberg
"""

# INITAL STEPS
# =============================================================================
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep
import csv
import re

# =============================================================================
# DEFINE FUNCTIONS
# =============================================================================

def search_url(url):
    """ Access url that allows search with chromedriver. """
    
    surl = url + '/search-middle-ns.asp'
    driver.get(surl)
    
    return

def switch_tab():
    """ Switch to results tab. """

    driver.switch_to.window(driver.window_handles[1])

    return

def search_sales():
    """ Search for sales after 1/1/2000. """
    
    elem = driver.find_element_by_id("SearchSaleDate")
    elem.send_keys('1/1/2000')
    go = driver.find_element_by_id("cmdGo")
    go.click()
    
    return

def read_data():
    ''' Read all the rows of sales data table. '''
    
    rows = driver.find_elements_by_xpath("/html/body/table[2]/tbody/tr")
    
    return rows

def access_error(url):
    """ Write error if url cannot be reached. """
    
    with open(r'C:\Anaconda3\VT_Scraper\errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        error = [url, 'access error']
        writer.writerow(error)    
    
    return

def search_error(url):
    """ Write error if url cannot be reached. """
    
    with open(r'C:\Anaconda3\VT_Scraper\errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        error = [url, 'search error']
        writer.writerow(error)    
    
    return

def read_error(url, count):
    """ Write error if no elements to read from table. """
    
    with open(r'C:\Anaconda3\VT_Scraper\errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        error = [url, 'read error', count]
        writer.writerow(error)
    
    return

def write_error(url):
    """ Write error if interuption writing rows to csv. """
    
    with open(r'C:\Anaconda3\VT_Scraper\errors.csv', 'a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        error = [url, 'write error']
        writer.writerow(error)
    
    return

def extract_data(url):
    '''Extracts elements into dataframe for each row.'''
    
    rows = read_data()
    for row in rows:
        # copy link text from first cell and extracts the account number from link
        link = row.find_element_by_css_selector('a').get_attribute('href')
        accnt = re.findall(r'\d+',link)[0]
        
        #each cell in row has td tag. assign text from each td tag to relevant variable 
        tds = row.find_elements_by_tag_name('td') 
        pid = tds[0].text
        addrs = tds[1].text
        owner = tds[2].text
        value = tds[4].text
        nhood = tds[8].text
        book = tds[10].text
        
        # build type and luc description have two elements seperated by <a> tags.
        # if there is no build year or type, ybuilt = '' and btype = 'na'
        try:
            build_type = tds[3].find_elements_by_tag_name('a')
            ybuilt = build_type[0].text
            try:
                btype = build_type[1].text
            except:
                btype = 'na'
        except:
            ybuilt = 'na'
            btype = 'na'
            
        try:
            luc_des = tds[7].find_elements_by_tag_name('a')
            luc = luc_des[0].text
            des = luc_des[1].text
        except:
            luc = 'na'
            des = 'na'
        
        # these cells have two variables stored in a single tag seperated by <br>
        try:
            bed_bath = tds[5].text.split()
            bed = bed_bath[0]
            bath = bed_bath[1]
        except:
            bed = 'na'
            bath = 'na'
        
        # when no lot or area present, lot = '' unit = '' and area = 'na'
        try:
            lot_area = tds[6].text.split()
            try:
                lot = lot_area[0]
                unit = lot_area[1]
            except:
                lot = 'na'
                unit = 'na'
            try:
                area = lot_area[2]
            except:
                area = 'na'
        except:
            lot = 'na'
            unit = 'na'
            area = 'na'
        
        # if there is no sale price listed, price = 'na'
        try:
            sale = tds[9].text.split()
            try:
                date = sale[0]
            except:
                date = 'na'
            try:
                price = sale[1]
            except:
                price = 'na'
        except:
            date = 'na'
            price = 'na'
            
        # assign each row to the new dataframe        
        new = pd.DataFrame([[url, link, pid, accnt, addrs, owner, ybuilt, btype, value, 
                           bed, bath, lot, unit, area, luc, des, nhood, date, price, book]], 
                         columns=['url', 'link','parcel', 'Account Number', 'Address', 
                                  'Owner', 'Year Built', 'Building Type', 'Total Value', 
                                  'Beds', 'Baths', 'Lot Size', 'Lot Units', 'Finished Area', 
                                  'LUC', 'LUC Description', 'Neighborhood', 'Sale Date', 
                                  'Sale Price', 'Book Page'])         
        
        # export each row to csv, report errors in error 
        try:
            new.to_csv('C:/Anaconda3/VT_Scraper/other_data.csv', mode='a', index=False, header=False)
        except:
            new.to_csv('C:/Anaconda3/VT_Scraper/write_errors.csv', mode='a', index=False, header=False)
            write_error(url)
            pass
    
    return

def next_page():
    """ Try to click the next page button. """
    
    try:
        driver.find_element_by_xpath("//*[contains(text(), 'Next Page')]").click()
        a = 'true'
    except:
        a = 'false'
    
    return a

def close_tab():
    ''' Closes out results tab and returns to initial search tab to enter next url. '''
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    return

# =============================================================================
# MAIN CODE BLOCK
# =============================================================================
# import list of urls
df = pd.read_csv(r'C:\Anaconda3\VT_Scraper\other_urls.csv')

#set path and open chromedrive
PATH = r'C:\Webdrivers\bin\chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH)

#initialize new data
new = pd.DataFrame(columns=['url', 'link','parcel', 'Account Number', 'Address', 
                            'Owner', 'Year Built', 'Building Type', 'Total Value', 
                            'Beds', 'Baths', 'Lot Size', 'Lot Units', 'Finished Area', 
                            'LUC', 'LUC Description', 'Neighborhood', 'Sale Date', 
                            'Sale Price', 'Book Page']) 

for index, row in df.iterrows():
    
    url = row['url']
    
    try:
        search_url(url)
    except:
        access_error(url)
        continue
    sleep(1)
    try:
        search_sales()
        switch_tab()
    except:
        search_error(url)
        continue
    
    a = 'true'
    count = 1    
    while a == 'true':            
        try:
            extract_data(url)
        except:
            read_error(url, count)
        
        
        a = next_page()
        print(url + '     ' + str(count))
        count += 1
    close_tab()