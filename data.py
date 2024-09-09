import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime as dt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import matplotlib.pyplot as plt
import os
from pathlib import Path
import time

def download():    
    ######################################################################################################################################
    ######################################### Download Country emission file #############################################################
    ######################################################################################################################################
    country_emissions = pd.read_csv('coal-mining_country_emissions.csv', parse_dates = ['start_time', 'end_time', 'created_date'])
    #Replace start time and end time with a single column, year
    country_emissions['year'] = country_emissions.apply(lambda row: row.start_time.year, axis = 1)
    country_emissions.rename(columns = {'iso3_country' : 'country'}, inplace = True)
    country_emissions.rename(columns = {'emissions_quantity' : 'emissions_quantity tonnes'}, inplace = True)
    print("""For Country emissions we drop columns with single values: 
    \tsector 	:  fossil-fuel-operations
    \tsubsector 	:  coal-mining
    \temissions_quantity_units 	:  tonnes
    \ttemporal_granularity 	:  annual
    \tmodified_date 	:  nan""")

    #created date : year 2023
    country_emissions = country_emissions[['country', 'year', 'gas', 'emissions_quantity tonnes']]
    country_emissions.to_csv('./modified data/country_emissions.csv')

    ######################################################################################################################################
    ######################################### Download Emission source file ##############################################################
    ######################################################################################################################################

    emissions_sources = pd.read_csv("coal-mining_emissions_sources.csv", parse_dates = ['start_time', 'end_time'])
    emissions_sources['year'] = emissions_sources.apply(lambda row: row.start_time.year, axis = 1)
    emissions_sources.drop(['start_time', 'end_time', 'other8', 'other8_def', "other9", "other9_def", "other10", "other10_def", 'modified_date'], inplace = True, axis = 1)
    dic_col = {}
    drop_list = []
    col = emissions_sources.columns
    print("\n\nFor Emission Source remove 'other' columns by renaming them with their descriptors\n")
    # renaming columns with "other" using their description, after removing null columns
    for c in col:
        if 'def' in c:
            dic_col[c.split('_')[0]] = emissions_sources[c].unique()[0].strip()
            print("column renamed to: ", emissions_sources[c].unique()[0].strip())
            drop_list.append(c)

    print("""remove columns that have single entry that describe data type-
    \tsector - fossil-fuel-operations
    \tsubsector - coal-mining
    \tactivity_units 	:  T of coal
    \tcapacity_units 	:  T per year 
    \tcreated_date 	:  2023-09-14 00:00:00
    \ttemporal_granularity :  annual\n\n""")
    
    drop_list += (['sector', 'subsector', 'activity_units', 'capacity_units', 'created_date', 'temporal_granularity', 'geometry_ref'])
    dic_col['iso3_country'] = 'country'
    dic_col['activity'] = 'activity T of coal'
    dic_col['capacity'] = 'capacity T per year'
    emissions_sources.rename(columns=dic_col, inplace = True)
    emissions_sources.drop(drop_list, inplace = True, axis = 1)
    #reorganize
    emissions_sources = emissions_sources[['source_id', 'source_name', 'source_type', 'country', 'year', 'lat', 'lon',
       'gas', 'emissions_quantity', 'activity T of coal',
       'emissions_factor', 'emissions_factor_units', 'capacity T per year',
       'capacity_factor', 'Coal Type', 'Coal Grade',
       'Total Reserves (Proven and Probable)',
       'Total Resource (Inferred, Indicated, Measured)',
       'Primary Consumer, Destination', 'Coal Plant, Steel Plant, Terminal',
       'Mine Depth']]
    
    emissions_sources['source_id'] = emissions_sources['source_id'].astype('str')
    emissions_sources.to_csv('./modified data/emissions_sources.csv')

    ######################################################################################################################################
    ######################################### Download Source ownership file #############################################################
    ######################################################################################################################################


    sources_ownership = pd.read_csv("coal-mining_emissions_sources_ownership.csv")

    print("""remove columns with single value
    \tsector 	:  fossil-fuel-operations
    \tsubsector 	:  coal-mining
    \trelationship 	:  owner
    \tinterest_units 	:  coal_reserves
    \tstart_date 	:  1/1/22 0:00
    \tend_date 	:  12/31/22 0:00
    \tmodified_date 	:  nan""")
    drop_list = ['geometry_ref', 'sector', 'subsector', 'relationship', 'interest_units', 'start_date', 'end_date', 'modified_date']
    sources_ownership.drop(drop_list, inplace = True, axis = 1)
    sources_ownership.rename(columns={'iso3_country' : 'country'}, inplace = True)
    sources_ownership.rename(columns={'percent_interest_company': 'percent_interest_company in coal_reserves'})
    sources_ownership = sources_ownership[['source_id', 'source_name', 'company_name', 'ultimate_parent_name', 'country', 
        'lat', 'lon', 'ultimate_parent_id', 'company_id','percent_interest_parent', 
        'percent_interest_company', 'percent_company_datasource', 'percent_parent_datasource', 
        'ultimate_parent_revenue_annual (mil)', 'created_date']]
    sources_ownership['source_id'] = sources_ownership['source_id'].astype('str')
    sources_ownership['ultimate_parent_id'] = sources_ownership['ultimate_parent_id'].astype('str')
    sources_ownership['company_id'] = sources_ownership['company_id'].astype('str')


    sources_ownership.to_csv('./modified data/source_ownership.csv')
    ######################################################################################################################################
    ######################################################################################################################################
    ######################################################################################################################################

    data = {'country_emissions' : country_emissions,
            'emissions_sources' : emissions_sources,
            'sources_ownership' : sources_ownership}

    return(data) 