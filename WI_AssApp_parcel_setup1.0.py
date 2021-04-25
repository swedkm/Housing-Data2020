# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 11:08:57 2020

@author: Kristen Swedberg
"""

import pandas as pd

chla = pd.read_csv(r'C:/LAGOS_Meta/WI/WI_Scraper/assap_bg_chla.csv', low_memory=False)
secchi = pd.read_csv(r'C:/LAGOS_Meta/WI/WI_Scraper/assap_bg_secchi.csv', low_memory=False)

dfc = chla[['STATEID', 'PARCELID', 'TAXPARCELID', 'PSTLADRESS', 'PLACENAME', 'PROPCLASS',
            'AUXCLASS', 'ASSDACRES', 'DEEDACRES', 'GISACRES', 'LONGITUDE', 'LATITUDE',
            'GEOID', 'B19013e1', 'GNIS_Name', 'lagoslakei', 'Name', 'Desig', 'County',
            'BLKGRPCE10', 'POINT_X', 'POINT_Y', 'DDLatLon']]
dfs = secchi[['STATEID', 'PARCELID', 'TAXPARCELI', 'PSTLADRESS', 'PLACENAME', 'PROPCLASS',
            'AUXCLASS', 'ASSDACRES', 'DEEDACRES', 'GISACRES', 'LONGITUDE', 'LATITUDE',
            'GEOID', 'B19013e1', 'GNIS_Name', 'lagoslakei', 'Name', 'Desig', 'County',
            'BLKGRPCE10', 'POINT_X', 'POINT_Y', 'DDLatLon']]
dfs = dfs.rename(columns={'TAXPARCELI': 'TAXPARCELID'})

df = pd.merge(dfc, dfs, how='outer')

df1 = df[df['PROPCLASS'] == '1']

info = pd.read_csv(r'C:/LAGOS_Meta/WI/WI_Scraper/assapp_info_initial1.csv')
info_desig = info['Desig'].str.upper()
info['Desig'] = info_desig

df2 = pd.merge(df1, info, on=['Name', 'County', 'Desig'])
df2.to_csv(r'C:/LAGOS_Meta/WI/WI_Scraper/assapp_parcel_url_setup.csv')