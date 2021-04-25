# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:18:40 2020

@author: swedkm
"""

import pandas as pd

#set paths
input_path = r'C:/LAGOS_Meta/Initial_Cleaning_GIS/NY/NY_Scraper/'
output_path = r'C:/LAGOS_Meta/Initial_Cleaning_GIS/NY/NY_Scraper2.0/URLs/'

#import url setup and merge with parcels to contrust unique URL's
imo_parcels = pd.read_csv(input_path + 'combined_imo_lf.csv', low_memory = False)
url_setup = pd.read_csv(input_path + 'url_setup.csv')

urls = pd.merge(imo_parcels, url_setup, how='left', on='IMO Municipality')

#subseting parcels that have different url constructions from rest.
#this may not be comprehensive list, only appies to lf.
sullivan = urls.loc[urls['IMO Municipality'] == 'Sullivan']
andes = urls.loc[urls['IMO Municipality'] == 'Andes']
jefferson = urls.loc[urls['IMO Municipality'] == 'Jefferson']
steuben = urls.loc[urls['IMO Municipality'] == 'Steuben']
rest = urls.loc[urls['IMO Municipality'] != 'Sullivan']
rest = rest.loc[rest['IMO Municipality'] != 'Andes']
rest = rest.loc[rest['IMO Municipality'] != 'Jefferson']
rest = rest.loc[rest['IMO Municipality'] != 'Steuben']

#processing Andes, Jefferson, and Steuben urls. All have same setup
a_urls = []
for index, row in andes.iterrows():
    try:
        a = str(row['str_sbl'])[:16]
    except:
        a = str(row['str_sbl'])
    u = str(row['rp1']) + str(row['rp2']) + str(row['str_swis']) + str(row['rp4']) + a + str(row['rp6']) + str(row['Residential Commercial Class']) + str(row['rp10'])
    a_urls.append(u)
andes['url'] = a_urls

j_urls = []
for index, row in jefferson.iterrows():
    try:
        a = str(row['str_sbl'])[:16]
    except:
        a = str(row['str_sbl'])
    u = str(row['rp1']) + str(row['rp2']) + str(row['str_swis']) + str(row['rp4']) + a + str(row['rp6']) + str(row['Residential Commercial Class']) + str(row['rp10'])
    j_urls.append(u)
jefferson['url'] = j_urls

st_urls = []
for index, row in steuben.iterrows():
    try:
        a = str(row['str_sbl'])[:16]
    except:
        a = str(row['str_sbl'])
    u = str(row['rp1']) + str(row['rp2']) + str(row['str_swis']) + str(row['rp4']) + a + str(row['rp6']) + str(row['Residential Commercial Class']) + str(row['rp10'])
    st_urls.append(u)
steuben['url'] = st_urls

#processing Sullivan urls
s_urls = []
for index, row in sullivan.iterrows():
    sbl = str(row['SBL']).replace(' ','')
    a = sbl[0:3]
    b = sbl[3:5]
    c = sbl[8:16]

    u = str(row['rp1']) + str(row['rp2']) + str(row['str_swis']) + str(row['rp4']) + a + str(row['rp6']) + b + c + str(row['rp8']) + str(row['Residential Commercial Class']) + str(row['rp10'])
    s_urls.append(u)
sullivan['url'] = s_urls

#processing remaining counties
r_urls = []
for index, row in rest.iterrows():
    if len(str(row['str_swis'])) == 6:
        u = str(row['rp1']) + str(row['rp2']) + str(row['str_swis']) + str(row['rp4']) + row['str_sbl'] + str(row['rp6']) + str(row['Residential Commercial Class']) + str(row['rp10'])
    if len(str(row['str_swis'])) == 5:
        u = str(row['rp1']) + str(row['rp2']) + '0' + str(row['str_swis']) + str(row['rp4']) + row['str_sbl'] + str(row['rp6']) + str(row['Residential Commercial Class']) + str(row['rp10'])
    r_urls.append(u)
rest['url'] = r_urls

#combining urls
parcel_urls = pd.concat([sullivan, andes, steuben, jefferson, rest]).drop_duplicates(subset='url')

#removing nonresidential properties from list
parcel_urls_res = parcel_urls.loc[parcel_urls['Residential Commercial Class'] == 'res']

#subsetting urls by SWIS and outputting
swis_urls = {}
swis_list = parcel_urls_res['SWIS'].drop_duplicates()
swis_list.to_csv(output_path + 'swis_list.csv', header=True)
for swis in swis_list:
    swis_urls[swis] = parcel_urls_res[parcel_urls_res['SWIS'] == swis]
    swis_urls[swis].to_csv(output_path + str(swis) + 'urls.csv')


#printing list of all urls
parcel_urls_res.to_csv(output_path + 'lf_parcel_urls.csv')