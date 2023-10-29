import customtkinter as ctk
import json, math
from datetime import datetime

class Tips():
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.logger = master.logger
        self.contents = {}
        self.male = {
            "Protein": [24.0, 52.0, 56.0],
            "Fat": [45, 70, 60],
            "Carbs": [90, 140, 130],
            "Calories": [1700, 2900, 2600],
            "Sugar": [22, 30, 36],
            "Fiber": [25, 31, 25],
            "Calcium": [1000, 1300, 1200],
            "Iron": [10, 8, 8],
            "Potassium": [2300, 2500, 3400],
            "Sodium": [1000, 1200, 1500],
            "Vitamin C": [35, 75, 90],
            "Cholesterol": [150, 150, 150]
        }
        self.female = {
            "Protein": [24.0, 46.0, 46.0],
            "Fat": [40, 60, 50],
            "Carbs": [80, 120, 100],
            "Calories": [1500, 2400, 2100],
            "Sugar": [22, 24, 26],
            "Fiber": [25, 26, 25],
            "Calcium": [1000, 1300, 1200],
            "Iron": [10, 15, 18],
            "Potassium": [2300, 2300, 2600],
            "Sodium": [1000, 1200, 1500],
            "Vitamin C": [35, 65, 75],
            "Cholesterol": [150, 150, 150]
        }
    
    def create_label(self, required: str, nutrient: str):
        self.label = ctk.CTkLabel(self.master, text=f"You should eat {required} {self.contents[nutrient][1]} more of {nutrient}")
        self.label.pack()
    
    def run(self, mainloop: bool = True) -> None:
        
        
        with open("json/user-data.json", "r") as f:
            data = json.load(f)
            age = int(datetime.today().year) - int(data["birth_year"])
            gender = data["gender"]
            self.logger.debug(age)
            self.logger.debug(gender)
            
        with open("json/food.json", "r") as f:
            # try:
                self.contents = json.load(f)
                group = 0
                if age > 8 and age < 18:
                    group = 1
                elif age > 18:
                    group = 2
                if gender == "Male":
                    for nutrient in self.male:
                        required = str(self.male[nutrient][group]-(self.contents[nutrient][0]/len(self.master.logged)))
                        if nutrient == "Protein":
                            print("quantum")
                            if abs(float(required)) > 10:
                                self.create_label(required, nutrient)
                        elif nutrient == "Fat":
                            if abs(float(required)) > 10:
                                self.create_label(required, nutrient)
                        elif nutrient == "Carbs":
                            if abs(float(required)) > 25:
                                self.create_label(required, nutrient)
                        elif nutrient == "Calories":
                            if abs(float(required)) > 400:
                                self.create_label(required, nutrient)
                        elif nutrient == "Sugar":
                            if abs(float(required)) > 5:
                                self.create_label(required, nutrient)
                        elif nutrient == "Fiber":
                            if abs(float(required)) > 5:
                                self.create_label(required, nutrient)
                        elif nutrient == "Calcium":
                            if abs(float(required)) > 300:
                                self.create_label(required, nutrient)
                        elif nutrient == "Iron":
                            if abs(float(required)) > 4:
                                self.create_label(required, nutrient)
                        elif nutrient == "Potassium":
                            if abs(float(required)) > 400:
                                self.create_label(required, nutrient)
                        elif nutrient == "Sodium":
                            if abs(float(required)) > 250:
                                self.create_label(required, nutrient)
                        elif nutrient == "Vitamin C":
                            if abs(float(required)) > 15:
                                self.create_label(required, nutrient)
                        elif nutrient == "Cholesterol":
                            if abs(float(required)) > 25:
                                self.create_label(required, nutrient)
            # except:
            #     pass
        ctk.CTkButton(
            self.master,
            text="Back to Homepage",
            command=self.master.quit
        ).pack()

        if mainloop:
            self.master.mainloop()