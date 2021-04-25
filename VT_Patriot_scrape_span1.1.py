# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:13:51 2020

@author: swedkm
"""

from selenium import webdriver
import pandas as pd
from time import sleep

def search_url(url):
    """ Access url that allows search with chromedriver. """

    surl = url + '/search-middle-ns.asp'
    driver.get(surl)

    return

def search_sales():
    """ Search for sales after 1/1/2000. """

    elem = driver.find_element_by_id("SearchSaleDate")
    elem.send_keys('1/1/2000')
    go = driver.find_element_by_id("cmdGo")
    go.click()

    return

vt = pd.read_csv('C:\HData_Process\VT\VT_Pat_Data.csv')

#set path and open chromedrive
PATH = r'C:\Webdrivers\bin\chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH)

#create dictionary of dataframes for each town
tnames = list(vt['Town'].value_counts().index)
d = {}
for t in tnames:
    d[t] = vt[vt.Town == str(t)]


#loop through each parcel in each dictionary.
#need to perform search first, then can access links
turls = list(vt['url'].value_counts().index)

url_index = 0
count = 0

for t in tnames:
    span = []
    url = turls[url_index]
    search_url(url)
    search_sales()

    for index, row in d[t].iterrows():
        count += 1
        print(count)
        link = row['link']
        try:
            driver.get(link)
            driver.switch_to_frame('bottom')
            print(link)
        except:
            s= 'bad link'
            continue
        try:
            s = driver.find_element_by_xpath('/html/body/form/div/table[1]/tbody/tr/td[2]/b/font').text
            print(s)
        except:
            s = 'na'
            print(s)
        span.append(s)

    d[t]['span'] = span
    d[t].to_csv('C:/Anaconda3/VT_Scraper/vt_data_span.csv', mode='a', index=False, header=False)
    url_index += 1


#need to do for auburn maine as well