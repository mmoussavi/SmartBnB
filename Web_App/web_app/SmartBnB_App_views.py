#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:02:38 2020

@author: mmoussavi
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:29:23 2020

@author: mmoussavi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:28:44 2020

@author: mmoussavi
"""
import numpy as np
from flask import request, render_template
from SmartBnB_functions import convert, price_boosters, feature_names, feature_display_names,num_extract, predict_price
from web_app import app


@app.route("/about/",methods=["POST", "GET"])
def about():
    return render_template('about.html')

@app.route("/contact/",methods=["POST", "GET"])
def contact():
    return render_template('contact.html')

@app.route("/")
@app.route("/predict/", methods=["POST", "GET"])
def predict():
    x_input=[]
    return render_template('input_form.html',x_input=x_input,feature_names=feature_names,feature_display_names=feature_display_names)

@app.route("/answer/", methods=["POST", "GET"])
def predict2():

    address=request.args.get('Distance_to_Downtown', '')
    global x_input
    x_input=[]
    x_input+=[address]
    num_vars = num_extract(request.args,1,4)
    x_input.extend(np.log(num_vars))
    neigh_vars = convert(request.args.get('neigh',"Chi_Neighborhood_Avondale"),4,24)
    x_input.extend(neigh_vars)
    prop_vars = convert(request.args.get('prop',"property_type_Apartment"),24,27)
    x_input.extend(prop_vars)
    room_vars = convert(request.args.get('room',"room_type_Entire home/apt"),27,30)
    x_input.extend(room_vars)
    global predictions
    predictions=predict_price(x_input)
    date = request.args.get('date',"01/06/2019")
    weekly, holiday, seasonal, total = price_boosters(date,predictions)

    return render_template('answer.html', x_input=x_input,
                                 feature_names=feature_names,
                                 prediction=predictions,
                                 feature_display_names=feature_display_names,
                                 total=total, weekly=weekly, holiday=holiday, seasonal=seasonal,date=date)
