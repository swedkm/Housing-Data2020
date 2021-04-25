# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:07:03 2020

@author: swedkm

Accurate Assessor
"""

import pandas as pd

chla = pd.read_csv(r'C:\Users\swedkm\Desktop\LAGOS_Meta\WI\accassess_res_chla.csv').drop(columns='OBJECTID')
secchi = pd.read_csv(r'C:\Users\swedkm\Desktop\LAGOS_Meta\WI\accassess_res_secchi.csv').drop(columns='OBJECTID')

df = pd.merge(chla, secchi, how='outer')

url_setup = pd.read_csv('C:\Anaconda3\WI_Scraper\lf_url_setup.csv')

df = pd.merge(df,url_setup, how='inner', on='Name')

urls = []

for index, row in df.iterrows():
    rt = row['Type']
    n = row['Name']
    p = str(row['PARCELID'])
    s = str(row['STATEID'])
    t = str(row['TAXPARCELID'])

    if rt == 'a':
        u = p
    elif rt == 'c':
        #if they have spaces in url it will be replaces with %
        u = p
    elif rt == 'd':
        u = p[3:]
    elif rt == 'e':
        u = p[4:]
    elif rt == 'f':
        u = p[6:]
    elif rt == 'g':
        u = t
    elif rt == 'h':
        u = t[4:]
    elif rt == 'i':
        u = t[6:]
    else:
        if n == 'WESCOTT':
            u = p[:3] + '-' + p[3:8] + '-' + p[8:]
        elif n == 'DAYTON':
            u = (p[4:6] + '-' + p[6:8] + '-' + p[8:10] + '-' + p[10:]).replace(' ','')
        elif n == 'GREEN VALLEY':
            u = p[2:5] + '-' + p[5:10] + '-' + p[10:]
        elif n == 'Cleveland':
            u = t.replace('.','')
        elif n == 'UPHAM':
            u = p[:3] + '-' + p[3:]
        elif n == 'Mosinee':
            u = p[3:7] + '-' + p[7:10] + '-' + p[10:]
        elif n == 'Sullivan':
            u = p[4:].replace('.','')

    init = str(row['Init'])

    urls.append(init + u)

df['url'] = urls

df.to_csv('F:\WI_Results\lf_urls.csv')

