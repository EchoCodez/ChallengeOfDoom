import requests
import json
from utils import constants


# from utils import WeatherInfo, UseLogger




# class WeatherData(UseLogger):
class WeatherData:
    def __init__(self) -> None:
        pass
    def weather(self) -> None:
        with open ("json/user-data.json", "r") as f:
            contents = json.load(f)
            lat = contents["location"]["latitude"]
            lon = contents["location"]["longitude"]

        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid=ae87b8e94884025fe72320419bba15eb'
       
        try:
            weatherResult = requests.get(
                url
            )
            
        except requests.exceptions.JSONDecodeError as e:
            exit(0)


        with open(constants.WEATHER_DATA, "w") as f:
            f.write(json.dumps(weatherResult.json(), indent=4))

        url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=ae87b8e94884025fe72320419bba15eb'

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