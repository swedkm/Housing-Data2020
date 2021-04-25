# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 18:01:38 2019

@author: swedkm
"""

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time

#importing list of parcel numbers and converting to list for loop
df = pd.read_csv('C:\Anaconda3\MN_Scraper\OtterTail\OtterTail_Parcels.csv')
parcels = list(df['Parcel'])

#enter main loop for each parcel
for parcel in parcels:
    
    #setting url including parcel number  
    url = 'https://www.ottertailcounty.us/ez/publicparcel_salesdetail.php?PIN=' + str(parcel)

    #accessing url. if ip fails wait 2 minutes and try again. if not print error. 
    try:
        response = requests.get(url)
    except:
        time.sleep(120)
        try:
            response = requests.get(url)
        except:
            print('error: ' + parcel)
            continue
    
    #downloading content
    content = BeautifulSoup(response.content, "html.parser")
    
    #finding all sales data tables
    cont = content.find_all('table', attrs={'width':'100%', 'border':'0', 
                                            'cellspacing':'2', 'cellpadding':'2'})
    
    #creating an array of values for each sales table
    #counting the number of sales records
    value = []
    count = 0
    for c in cont:                                        
        value_table = c.find_all(['span'], attrs={'class':'style13'})
        value.append(value_table)
        count += 1
    
    #assessing the table for each sale record table and assigning values to dictionary
    sales_count = list(range(count))
    sales = {}
    final_v = {}
    for s in sales_count[1:]:
        sales['val_' + str(s)] = [str(parcel)]
        for j in value[s][1:]:    
            v = str(j.text)
            v = " ".join(v.split())
            sales['val_' + str(s)].append(v)
        sales['val2_' + str(s)] = sales['val_' + str(s)][0:13]
        
        #if sale data is na, then skip the parcel
        if sales['val2_' + str(s)][1] == "":
            continue
        
        #if additional parcels in sale record, combine them into a list
        if len(sales['val_' + str(s)]) > 13:
            sales['parcels'] = []
            for k in sales['val_' + str(s)][12:]: 
                sales['parcels'].append(k) 
            final_v['val2_' + str(s)] = sales['val_' + str(s)][0:12]
            final_v['val2_' + str(s)].append(str(sales['parcels']))
        
        #if no additional parcels, print original values
        else:
            final_v['val2_' + str(s)] = sales['val_' + str(s)][0:12]
            final_v['val2_' + str(s)].append('na')
        
    #writing each sale to seperate rows for each parcel
    with open('C:\Anaconda3\MN_Scraper\OtterTail\sales_details.csv','a') as write_file:
        writer = csv.writer(write_file, lineterminator='\n')
        for v in final_v:
            writer.writerow(final_v[str(v)])