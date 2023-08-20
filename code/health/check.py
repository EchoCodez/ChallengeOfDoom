import requests
import json
from logging import Logger

class Algorithm:
    def __init__(self, food: str, quantity: str, logger: Logger) -> None:
        self.food = food
        self.quantity = quantity
        self.logger = logger
    
    def get_nutrition_info(self, api_key: str):
        params = {
            "query": self.food,
            "api_key": api_key,
        }

        response = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search", params=params)
        response_data = response.json()


        if "foods" not in response_data or not response_data["foods"]:
            print("Food not found.")
            return None

        food_id = response_data["foods"][0]["fdcId"]

        response = requests.get(f"https://api.nal.usda.gov/fdc/v1/food/{food_id}", params={"api_key": api_key})
        raw_data = response.json()
        food_details = raw_data["foodNutrients"]
        nutrients = {}
        for detail in food_details:
            if detail["nutrient"]["name"] == "Energy":
                nutrients["Calories"] = [float(detail["amount"])*self.quantity/100, detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Protein":
                nutrients["Protein"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Sugars, total including NLEA":
                nutrients["Sugar"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Calcium, Ca":
                nutrients["Calcium"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Iron, Fe":
                nutrients["Iron"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Fiber, total dietary":
                nutrients["Fiber"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Cholesterol":
                nutrients["Cholesterol"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Carbohydrate, by difference":
                nutrients["Carbs"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Potassium, K":
                nutrients["Potassium"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Total lipid (fat)":
                nutrients["Fat"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Sodium, Na":
                nutrients["Sodium"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Vitamin C, total ascorbic acid":
                nutrients["Vitamin C"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Vitamin A, IU":
                nutrients["Vitamin D"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
            if detail["nutrient"]["name"] == "Vitamin D (D2 + D3), International Units":
                nutrients["Vitamin D"] = [float(detail["amount"]*self.quantity/100), detail["nutrient"]["unitName"]]
        with open("json/food.json", "r") as f:
            try:
                contents = json.load(f)
                empty = False
            except:
                empty = True
        with open("json/food.json", "w") as f:
            if not empty:
                contents["Calories"][0] += nutrients["Calories"][0]
            else:
                json.dump(nutrients, f, indent=4)
        return raw_data["foodNutrients"]

    def run(self):
        api_key = "4aoCShlfHPImyLqzhxPHpSGnFVadB92vgwX5cE56"

        nutrition_info = self.get_nutrition_info(api_key)
        if nutrition_info:
            print("Nutrition Information:")
            for info in nutrition_info:
                try:
                    self.logger.debug(f"{info['nutrient']['name']} : {info['amount']} {info['nutrient']['unitName']}")
                except:
                    pass
    