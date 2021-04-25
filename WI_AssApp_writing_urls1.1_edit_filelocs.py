# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:07:03 2020

@author: swedkm

Accurate Assessor
"""

import pandas as pd

chla = pd.read_csv(r'C:\LAGOS_Meta\WI\WI_Scraper\accassess_res_chla.csv', low_memory=False)
secchi = pd.read_csv(r'C:\LAGOS_Meta\WI\WI_Scraper\accassess_res_secchi.csv', low_memory=False)

#df = pd.merge(chla, secchi, how='outer')

url_setup = pd.read_csv('C:\LAGOS_Meta\WI\WI_Scraper\lf_url_setup.csv')

df_secchi = pd.merge(secchi,url_setup, how='inner', on='Name')
df_chla = pd.merge(chla,url_setup, how='inner', on='Name')

urls = []

for index, row in df_secchi.iterrows():
    rt = row['Type']
    n = row['Name']
    p = str(row['PARCELID'])
    s = str(row['STATEID'])
    t = str(row['TAXPARCELI'])

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

df_secchi['url'] = urls

df_secchi.to_csv(r'C:\LAGOS_Meta\WI\WI_Scraper\accassess_secchi_urls.csv')

#########################################################################################3
#repeat above for chla

urls = []

for index, row in df_chla.iterrows():
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

df_chla['url'] = urls

df_chla.to_csv(r'C:\LAGOS_Meta\WI\WI_Scraper\accassess_chla_urls.csv')

