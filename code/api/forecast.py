import requests
import json
import ast

# from utils import WeatherInfo, UseLogger


# class WeatherData(UseLogger):
class WeatherData:
    def make_call(self):
        url = 'https://api.ambeedata.com/latest/pollen/by-lat-lng?lat=37.54068&lng=-77.43367'
        result = requests.get(
            url,
            headers = {
                "x-api-key": "4fdc231b972e03b1df86d489299f2c39c62375be477304012f912fae0039a3a8",
                "Content-type": "application/json"
                }
        ).json()
        
        with open("json/pollen.json", "w") as f:
            f.write(json.dumps(result, indent=4))
    

            
        # print('Grass Pollen Count: ' + str(eval(result)['data'][0]['Count']['grass_pollen']))
        # print('Tree Pollen Count: ' + str(eval(result)['data'][0]['Count']['tree_pollen']))
        # print('Weed Pollen Count: ' + str(eval(result)['data'][0]['Count']['weed_pollen']))
        # print('Grass Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['grass_pollen']))
        # print('Tree Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['tree_pollen']))
        # print('Weed Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['weed_pollen']))
        
print(WeatherData().make_call())