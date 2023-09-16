import requests
import json
from utils import constants


# from utils import WeatherInfo, UseLogger




# class WeatherData(UseLogger):
class WeatherData:
    def weather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather?lat=37.43&lon=-78.66&units=metric&appid=ae87b8e94884025fe72320419bba15eb'
       
        try:
            weatherResult = requests.get(
                url
            )
        except requests.exceptions.JSONDecodeError as e:
            exit(0)


        with open(constants.WEATHER_DATA, "w") as f:
            f.write(json.dumps(weatherResult.json(), indent=4))

        url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat=-78.66&lon=37.43&appid=ae87b8e94884025fe72320419bba15eb'

        try:
            airQuality = requests.get(
                url
            )
        except requests.exceptions.JSONDecodeError as e:
            exit(0)

        with open(constants.AIR_QUALITY, "w") as f:
            f.write(json.dumps(airQuality.json(), indent=4))


           
        # print('Grass Pollen Count: ' + str(eval(result)['data'][0]['Count']['grass_pollen']))
        # print('Tree Pollen Count: ' + str(eval(result)['data'][0]['Count']['tree_pollen']))
        # print('Weed Pollen Count: ' + str(eval(result)['data'][0]['Count']['weed_pollen']))
        # print('Grass Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['grass_pollen']))
        # print('Tree Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['tree_pollen']))
        # print('Weed Pollen Risk: ' + str(eval(result)['data'][0]['Risk']['weed_pollen']))


if __name__ == "__main__":
    print(WeatherData().weather())