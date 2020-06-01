#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:20:04 2020

@author: mmoussavi
"""

"""
This file contains the functionality required in SmartBnB_App_Views.py
"""

import pickle
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance, Point


with open("web_app/static/models/elas_model_Jan28_2020.pkl", "rb") as f:
    my_model = pickle.load(f)
with open("web_app/static/data/Chicago_price_change_df.pickle","rb") as g:
    price_change_df = pickle.load(g)

feature_names = my_model.feature_names
feature_display_names = my_model.feature_display_names


def get_latlon_from_address(address):
    geolocator = Nominatim(user_agent="data_science_project", timeout=3)
    city = "Chicago"
    country = "USA"
    location = geolocator.geocode(address+' '+city+' '+country)
    return(location.latitude, location.longitude)

def distance_to_downtown(lat, lon):
    downtown = Point(41.8841262, -87.6214286)
    point_of_interest = Point(float(lat), float(lon))
    d_downtown = distance.distance(point_of_interest, downtown).miles
    return(d_downtown)

def num_extract(inputs,start,end):
    """
    Input:
    feature_dict: a dictionary of the form {"feature_name": "value"}

    Output:
    Returns list with the values corresponding to the start and end indices
    """
    out = [float(inputs.get(name, 0)) for name in my_model.feature_names[start:end]]
    return out


def predict_price(x_in):
    address=x_in[0]
    lat, lon=get_latlon_from_address(address)
    Distance_City_Center=distance_to_downtown(lat, lon)
    x_in[0]=np.log(Distance_City_Center)
    X_sam1=pd.DataFrame([x_in], columns=list(feature_names))
    price_predicted=np.exp(my_model.predict(X_sam1))
    final=round(price_predicted[0])
    return final


def convert(string,start,end):
    """
    Input: string for selected field, start/end index in feature column set
    Output: list of values corresponding to X_test[start:end]
    """
    vars = np.zeros(end-start)
    if string == "Other":
        return vars
    elif string in feature_names[start:end]:
        vars[list(feature_names[start:end]).index(string)] = 1
        return list(vars)


def price_boosters(date_string, price):
    """
    Calculate price boosters for time of year, day of week, and holidays
    """
    date = pd.to_datetime(date_string)
    if date > price_change_df.ds.max():
        date_string = date_string[0:-4] + '2020'
        date = pd.to_datetime(date_string)
    if date < price_change_df.ds.min():
        date_string = date_string[1:-4] + '2019'
        date = pd.to_datetime(date_string)
    boosters = price_change_df[price_change_df.ds == date][[
        'weekly_percentage', 'holiday_percentage', 'yearly_percentage'
    ]].values[0]
    weekly = round(boosters[0] * price, 2)
    holiday = round(boosters[1] * price, 2)
    seasonal = round(boosters[2] * price, 2)
    total = round(price + weekly + holiday + seasonal,2)
    return weekly, holiday, seasonal, total


if __name__ == '__main__':
    from pprint import pprint
    print("Checking to see what setting all params to 0 predicts")
    features = {f: '0' for f in feature_names}
    print('Features are')
    pprint(features)

    x_in, probs = predict_price(features)
    print(f'Input values: {x_in}')
    print('Output probabilities')
    pprint(probs)
