# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 23:23:50 2020

@author: swedkm
"""

import geopandas as gpd
import pandas as pd
import os
from multiprocessing import Pool

def clean_sales_shp(county):

    #create a directory for each county folder and set the path
    directory = 'C:\Anaconda3\MN_Scraper\Metro_Region\MN_Metro_Shapes_2002_2015\Output/' + county
    folder = os.listdir(directory)
    path = [os.path.join(directory, s) for s in folder if '.shp' in s]

    #set coordinate reference system to the crs in the first shapefile
    coord = str(gpd.read_file(path[0]).crs)

    #concatenate shapefiles into 1 aggregated shapefile
    agrt = gpd.GeoDataFrame(pd.concat([gpd.read_file(p) for p in path]), crs=coord)

    #edit aggregated shapefile to remove duplicate sales
    agrt = agrt.drop_duplicates()

    #identify relevant sales to go into sales geodataframe
    keep_sale = []
    sale_year = []
    sale_month = []
    address = []
    full_address = []

    for index, row in agrt.iterrows():

        value = row['SALE_VALUE']

        try:
            date = row['SALE_DATE'].split('/')
            year = date[2]
            month = date[0]
        except:
            try:
               date = row['SALE_DATE'].split('-')
               year = date[2]
               month = date[0]
            except:
                year = 0
                month = 0

        addrs = str(row['BLDG_NUM']) + ' ' + str(row['STREETNAME']) + ' ' + str(row['STREETTYPE']) + ' ' + str(row['SUFFIX_DIR'])

        faddrs = addrs + ', ' + str(row['CITY']) + ', MN, ' + str(row['ZIP'])

        use = row['USE1_DESC']
        multi = row['MULTI_USES']
        dwell = row['DWELL_TYPE']

        if value == 0:
            keep = 'no'
        elif year < 2001 | year > 2015:
            keep = 'no'
        elif use != '100 Res 1 unit':
            keep = 'no'
        elif dwell != 'Single-Family / Owner Occupied':
            keep = 'no'
        elif multi != 'N':
            keep = 'no'
        else:
            keep = 'yes'

        keep_sale.append(keep)
        sale_year.append(year)
        sale_month.append(month)
        address.append(addrs)
        full_address.append(faddrs)

    agrt['Keep Sale'] = keep_sale
    agrt['Sale Year'] = sale_year
    agrt['Sale Month'] = sale_month
    agrt['Street Address'] = address
    agrt['Full Address'] = full_address

    sales = agrt[agrt['Keep Sale'] == 'yes']

    output_file1 = 'C:\Anaconda3\MN_Scraper\Metro_Region\MN_Metro_Shapes_2002_2015\Output/' + county + '_clean.shp'
    sales.to_file(output_file1)


################################### MAIN CODE BLOCK ######################################

if __name__ == "__main__":

    county = ['Anoka', 'Carver', 'Dakota', 'Ramsey', 'Scott', 'Washington']

    p = Pool(3)
    result = p.map(clean_sales_shp, county)
    p.terminate()
    p.join()