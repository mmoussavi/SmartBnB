# SmartBnB
Inisght Data Science Project: http://smartbnb.live/

![](ReadMe_Images/SmartBnB_Web.png)

# Background
With the revenue generation opportunities airbnb offers, more and more people are interested in becoming hosts,
however, this potential for revenue generation is only realized with the right pricing strategies. Overpricing results in low booking rates and underpricing directly results in loss of revenue.

<img src="/ReadMe_Images/Pricing.png" width=300 class="center">

So pricing is very important but it can also be a very confusing process.
While Airbnb offers some general guidelines, there are currently no free, flexible, and reliable tools that provide pricing strategies to new hosts.

That’s exactly what SmartBnB provides!
Its user base will be new hosts in Chicago, and it’s goal is to help maximize their revenue by providing smart pricing based on data from their successful competitors.
In other words, I built my models based on listings with high occupancy rates and high review scores so that suggested listing price will yield high booking rates as well.

<img src="/ReadMe_Images/Successful_competitors.png" width=400>

# Data
To build this app, I scraped Chicago airbnb data from a third-party database, called insideairbnb (http://insideairbnb.com/about.html). There were around 100 features available in the dataset, I removed uninformative features, engineered new ones such as distance to downtown from address, and different categories of amenities,..then I removed collinear features and what ended up going into my final model were 30 features related to property attributes.

# SmartBnB pipeline

Smartbnb’s pricing tool has two major components.
The first component is a machine learning model that calculates a base price according to property information, 
and the second one is a forecast model that modifies the base price as a function of date. 
The final results are then served to the user in a flask app hosted on an AWS.

![](ReadMe_Images/SmartBnB_Pipeline.png)
