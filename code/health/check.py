import requests
import json

class Algorithm:
    def __init__(self, food: str) -> None:
        self.food = food
    
    def get_nutrition_info(self, food: str, api_key):
        base_url = "https://api.nal.usda.gov/fdc/v1/"
        search_url = base_url + "foods/search"
        details_url = base_url + "food/{}/"

        params = {
            "query": food,
            "api_key": api_key,
        }

        response = requests.get(search_url, params=params)
        response_data = response.json()


        if "foods" not in response_data or not response_data["foods"]:
            print("Food not found.")
            return None

        food_id = response_data["foods"][0]["fdcId"]

        response = requests.get(details_url.format(food_id), params={"api_key": api_key})
        food_details = response.json()

        with open("json/food.json", "w") as f:
            json.dump(food_details, f, indent=4)

        return food_details["foodNutrients"]

    def run(self):
        api_key = "4aoCShlfHPImyLqzhxPHpSGnFVadB92vgwX5cE56"

        nutrition_info = self.get_nutrition_info(self.food, api_key)
        if nutrition_info:
            print("Nutrition Information:")
            for info in nutrition_info:
                try:
                    print(f"{info['nutrient']['name']} : {info['amount']} {info['nutrient']['unitName']}")
                except:
                    pass
    