# TP2 Sistemas de computación

Grupo : Santiago Recalde - Joaquín Otalora - Federico Richter

## Request a API

Comenzamos generando una request a la API del Banco Mundial donde se encuentran los índices de GINI medidos en los países desde el año 2011 hasta el 2019. Haciendo uso del módulo requests de python, hacemos una petición GET para obtener todos los datos en forma de JSON y guardarlos en la variable llamada data. Luego iremos iterando sobre todos los elementos del objeto JSON y si vemos que los datos pertenecen a Argentina los agregamos a un arreglo llamado index_argentina. Todo esto envuelto en try-except, el cual sirve como except handler en caso de, como dice el nombre, ocurra una excepción a la hora de requerir los datos a la API  : 
```python
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
    	if (country_name == "Argentina") :
    		if item["value"] == None:
    			index_argentina.append(0.0)
    		else:
    			index_argentina.append(item["value"])
    		count = count + 1
    	indicator_value = item["value"]
    	year = item["date"]

except requests.RequestException as e:
    print(f"Error fetching data: {e}")
