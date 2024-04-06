import requests
import numpy as np
from calculator import calculator


api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

try:
    response = requests.get(api_url) #get request from api
    response.raise_for_status()  # Check for any errors

    data = response.json()
    count = 0
    index_argentina = []

    for item in data[1]:  
    	country_name = item["country"]["value"]
    	if country_name == "Argentina":
    		index_argentina.append(item["value"])
    		count = count + 1
    	indicator_value = item["value"]
    	year = item["date"]
    	#print(f"Country: {country_name}, Year: {year}, GINI Index: {indicator_value}")

    print(f"Argentina GINI Index in : {index_argentina[0]}")
    print(calculator(index_argentina))


except requests.RequestException as e:
    print(f"Error fetching data: {e}")