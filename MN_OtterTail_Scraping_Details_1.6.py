# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:31:20 2019

@author: swedkm
"""

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time

#importing list of parcel numbers and converting to list for loop
df = pd.read_csv('C:\Anaconda3\MN_Scraper\OtterTail\Parcels_GIS.csv')
df = df.drop_duplicates(subset=['Parcel'])

#creating list of parcels
parcels = []
for index, row in df.iterrows():
    a = row['Parcel']
    try: 
        p = int(a)
        s = str(p)
        parcels.append(a)
    except:
        pass

#enter main loop for each parcel
for parcel in parcels:
    
    #setting url including parcel number  
    url = 'https://www.ottertailcounty.us/ez/publicparcel_full.php?PIN=' + parcel

    #accessing url. if ip fails wait 2 minutes and try again. if not print error. 
    try:
        response = requests.get(url)
    except:
        time.sleep(120)
        try:
            response = requests.get(url)
        except:
            continue
    
    #downloading content
    content = BeautifulSoup(response.content, "html.parser")
    
    #finding all data tables
    #0 = Detailed Results
    #1 = Summary Data
    #2 = Land Data
    #4 = Bulding(s) Detail (need to check on how this works with land only)
    #5 = Additional Property Details
    cont = content.find_all('table', attrs={'width':'100%', 'border':'0', 'cellspacing':'2', 'cellpadding':'2'})
    
    #creating arrays of tags with relevant attributes for each table
    value = []
    for c in cont:                                        
        value_table = c.find_all(['td', 'div', 'span'], attrs={'class':'style13'})
        value.append(value_table)

###############################################################################
    #creating a dictionary with values for Detailed Results (dr)
    dr = {}
    dr['val'] = []
    for j in value[0]:
        v = str(j.text)
        v = " ".join(v.split())
        dr['val'].append(v)

    #creating a dictionary with values for Summary Data (sd)
    sd = {}
    sd['val'] = []
    for j in value[1]:
        v = str(j.text)
        v = " ".join(v.split())
        sd['val'].append(v)
    
    #testing whether more than 1 record is included in summary data
    #if multiple records, move to next parcel
    if len(sd['val']) > 15:
        print('multiple records: ' + parcel)
        continue

    #creating a dictionary with values for Land Details (ld)
    ld = {}
    ld['val'] = []
    for j in value[2]:
        ld['val'].append(v)
    
    #checking the number of records and appending na values as neccessary
    #if more than 10 records will return an error for additional records
    ld['final'] = [] 
    ld['final'].extend(ld['val'])
    remain = 160 - len(ld['val'])
    if remain >= 0:
        i = 0
        while i < remain:
            ld['final'].append('')
            i += 1
        ld['final'].append('')
    else:
        ld['final'].append('l_error')

###############################################################################
    #testing if there are building details in record
    #if yes continue through steps
    if len(value) >= 6:
        #creating a dictionary with values for Building Details (bd)
        bd = {}
        bd['val'] = []
        for j in value[4]:
            v = str(j.text)
            v = " ".join(v.split())
            bd['val'].append(v)
        
        #removing values that I don't need (initial index - post replacement index)
        bd['val'].pop(0)
        bd['val'].pop(1-1)
        bd['val'].pop(2-2)
        bd['val'].pop(4-3)
        
        #checking the number of records and appending na values as neccessary
        #if more than 10 records will return an error for additional records
        bd['final'] = [] 
        bd['final'].extend(bd['val'])
        remain = 128 - len(bd['val'])
        if remain >= 0:
            i = 0
            while i < remain:
                bd['final'].append('')
                i += 1
            bd['final'].append('')
        else:
            bd['final'].append('b_error')
    
        #creating a dictionary with values for Additional Features on Property (ad)
        ad = {}
        ad['val'] = []
        for j in value[6]:
            v = str(j.text)
            v = " ".join(v.split())
            if v == '':
                v = 'blank'
            ad['val'].append(v)
        
        #removing blank lines at end of list
        blanks = ad['val'].count('blank')
        if blanks > 0:
            i = -1
            while i < blanks - 1:
                ad['val'].remove('blank')
                i += 1
            
        #checking the number of records and appending na values as neccessary
        #if more than 10 records will return an error for additional records
        ad['final'] = [] 
        ad['final'].extend(ad['val'])
        remain = 140 - len(ad['val'])
        if remain >= 0:
            i = 0
            while i < remain:
                ad['final'].append('')
                i += 1
            ad['final'].append('')
        else:
            ad['final'].append('a_error')
###############################################################################    
    #if there are not building details in record
    else:
        #creating an empty array for buildings details to add to row in csv
        bd = {}
        bd['val'] = []
        bd['final'] = []
        remain = 128 - len(bd['val'])
        if remain >= 0:
            i = 0
            while i < remain:
                bd['final'].append('')
                i += 1
            bd['final'].append('')
        else:
            bd['final'].append('b_error')
    
        #creating a dictionary with values for Additional Features on Property (ad)
        ad = {}
        ad['val'] = []
        for j in value[4]:
            v = str(j.text)
            v = " ".join(v.split())
            if v == '':
                v = 'blank'
            ad['val'].append(v)
        
        #removing blank lines at end of list
        blanks = ad['val'].count('blank')
        if blanks > 0:
            i = -1
            while i < blanks - 1:
                ad['val'].remove('blank')
                i += 1
            
        #checking the number of records and appending na values as neccessary
        #if more than 10 records will return an error for additional records
        ad['final'] = [] 
        ad['final'].extend(ad['val'])
        remain = 140 - len(ad['val'])
        if remain >= 0:
            i = 0
            while i < remain:
                ad['final'].append('')
                i += 1
            ad['final'].append('')
        else:
            ad['final'].append('error')
###############################################################################
    #combining values into one array to print as row in csv
    details = []
    details.append(parcel)
    details.extend(dr['val'])
    details.extend(sd['val'])
    details.extend(ld['final'])
    details.extend(bd['final'])
    details.extend(ad['final'])
    
    #csv with preset header to include columns for 10 records in ld, bd, and ad
    try:
        with open('C:\Anaconda3\MN_Scraper\OtterTail\parcel_details_final.csv','a') as write_file:
            writer = csv.writer(write_file, lineterminator='\n')
            writer.writerow(details)
    except:
        pass