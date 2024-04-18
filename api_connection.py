import requests
from calculator import calculator
import timeit

import matplotlib.pyplot as plt

def fetch_data():
    api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

    try:
        response = requests.get(api_url)  # get request from api
        response.raise_for_status()  # Check for any errors

        data = response.json()
        count = 0
        index_argentina = []

        for item in data[1]:
            country_name = item["country"]["value"]
            if country_name == "Argentina":
                if item["value"] == None:
                    index_argentina.append(0.0)
                else:
                    index_argentina.append(item["value"])
                    count = count + 1
            indicator_value = item["value"]
            year = item["date"]

        print(f"Argentina GINI Index antes del calculo en C:")
        print(index_argentina)
        res = calculator(index_argentina)
        print(f"Argentina GINI Index luego del calculo en C: ")
        print(res)
        plt.plot(res)
        plt.xlabel('Year')
        plt.ylabel('GINI Index')
        plt.title('Argentina GINI Index over Time')
        #plt.show()

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

execution_times = []
for _ in range(1000):
    start_time = timeit.default_timer()
    fetch_data()
    execution_time = timeit.default_timer() - start_time
    execution_times.append(execution_time)

average_time = sum(execution_times) / len(execution_times)
print(f"Promedio de tiempo de ejecución: {average_time} segundos")