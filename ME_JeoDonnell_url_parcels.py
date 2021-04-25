# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:28:24 2020

@author: swedkm
"""

import pandas as pd

secchi = pd.read_csv(r'C:/LAGOS_Meta/ME/Housing Data/Process/jeo/secchi_lf_parcels.csv')
chla = pd.read_csv(r'C:/LAGOS_Meta/ME/Housing Data/Process/jeo/chla_lf_parcels.csv')

df = pd.concat([secchi, chla])
df2 = df.drop_duplicates(subset='STATE_ID')

street_address = []
full_address = []
url = []
keep = []

for index, row in df2.iterrows():

    #wirting urls
    if (row['TOWN'] == 'Acton' or row['TOWN'] == 'Boothbay' or row['TOWN'] == 'Canton'
        or row['TOWN'] == 'Chelsea' or row['TOWN'] == 'Greenwood' or row['TOWN'] == 'Hartford'
        or row['TOWN'] == 'Sebago'):

        pid = row['STATE_ID'].split('_')
        u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + pid[1]

    elif row['TOWN'] == 'Bridgton':
        pid = row['MAP_BK_LOT'].split('-')
        l = len(pid)
        if l == 2:
            try:
                p = str(int(pid[0])) + '-0-' + str(int(pid[1])) + '-0'
                u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p
            except:
                u = 'na'
        elif l == 3:
            try:
                p = str(int(pid[0])) + '-' + str(int(pid[1])) + '-' + str(int(pid[2])) + '-0'
                u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p
            except:
                u = 'na'
        else:
            u = 'na'

    elif row['TOWN'] == 'Fryeburg':
        pid = row['STATE_ID'].split('_')
        pi = pid[1].split('-')
        l = len(pi)
        if l == 2:
            try:
                p = str(pi[0]) + '-' + str(pi[1]) + '-000-000'
                u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p
            except:
                u = 'na'
        elif l == 3:
            try:
                p = str(pi[0]) + '-' + str(pi[1]) + '-' + str(pi[2]) + '-000'
            except:
                u = 'na'
        else:
            u = 'na'

    elif row['TOWN'] == 'Limerick':
        pid = row['STATE_ID'].split('_')
        pi = pid[1].split('-')
        l = len(pi)
        if l == 2:
            try:
                p = str(pi[0]) + '-' + str(pi[1]) + '-0-0'
                u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p
            except:
                u = 'na'
        elif l == 3:
            try:
                p = str(pi[0]) + '-' + str(pi[1]) + '-' + str(pi[2]) + '-0'
            except:
                u = 'na'
        else:
            u = 'na'

    elif row['TOWN'] == 'Naples':
        pid = row['MAP_BK_LOT'].replace('-0', '-')
        u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + pid

    elif row['TOWN'] == 'Shapleigh':
        pid = row['STATE_ID'].split('_')
        pi = pid[1]
        p = str(pi[:3]) + '-' + str(pi[3:6])
        u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p

    elif row['TOWN'] == 'Sweden':
        pid = row['STATE_ID'].split('_')
        pi = pid[1].split('-')
        try:
            if len(pi[1]) == 1:
                p2 = '0' + str(pi[1])
            else:
                p2 = str(pi[1])
            p = pi[0] + '-' + p2 + '-' + pi[2]
            u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p
        except:
            u = 'na'

    elif row['TOWN'] == 'Turner':
        pid = row['STATE_ID'].split('_')
        pi = pid[1]
        p = '0' + str(pi[:2]) + '-0' + str(pi[2:4]) + '-' + str(pi[4:7]) + '-' + str(pi[7:])
        u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p

    elif row['TOWN'] == 'Woodstock':
        pid = row['STATE_ID'].split('_')
        pi = pid[1].split('-')
        try:
            if len(pi[0]) == 2:
                p0 = '0' + str(pi[0])
            else:
                p0 = '00' + str(pi[0])
                if len(pi[1]) == 2:
                    p1 = '-0' + str(pi[1])
                else:
                    p1 = '-00' + str(pi[1])
            try:
                test = int(pi[2])
                if test == 0:
                    p2 = ''
                elif len(pi[2]) == 2:
                    p2 = '-0' + str(pi[2])
                else:
                    p2 = '-00' + str(pi[2])
            except:
                p2 = '-' + str(pi[2])
            p = p0 + p1 + p2
            u = 'http://jeodonnell.com/cama/' + row['TOWN'] + '/' + p
        except:
            u = 'na'

    else:
        u = 'town typo'

    # writing address fields
    if (row['TOWN'] == 'Acton' or row['TOWN'] == 'Boothbay' or row['TOWN'] == 'Bridgton'
        or row['TOWN'] == 'Canton' or row['TOWN'] == 'Chelsea' or row['TOWN'] == 'Greenwood'
        or row['TOWN'] == 'Hartford' or row['TOWN'] == 'Sweden' or row['TOWN'] == 'Woodstock'):

        s = str(row['PROPLOCNUM']) + ' ' + row['PROP_LOC']
        f = s + ' ' + row['TOWN'] + ', ME'

    elif (row['TOWN'] == 'Naples' or row['TOWN'] == 'Sebago' or row['TOWN'] == 'Turner'):

        s = row['PROP_LOC']
        f = s + ' ' + row['TOWN'] + ', ME'

    else:
        s = 'na'
        f = 'na'

    # keeping parcels and blanks
    if row['TYPE'] == 'Parcel':
        k = 'yes'
    elif row['TYPE'] == " ":
        k = 'yes'
    else:
        k = 'no'
    if u == 'na':
        k = 'no'

    url.append(u)
    street_address.append(s)
    full_address.append(f)
    keep.append(k)

df2['Street Address'] = street_address
df2['Full Address'] = full_address
df2['url'] = url
df2['keep'] = keep

df3 = df2[df2['keep'] == 'yes']
df3.to_csv(r'C:/LAGOS_Meta/ME/Housing Data/Process/url_parcels.csv')
