import customtkinter as ctk
import json
from datetime import datetime
from calendar import monthrange
from logging import Logger
from health.check import Algorithm

class Calendar:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.key = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        }
        self.logger = self.master.logger
        self.days = []
    
    def run(self, mainloop: bool = True) -> None:
        today = datetime.today()
        offset, month = monthrange(today.year, today.month)
        
        for i in range(7):
            ctk.CTkLabel(
                self.master,
                text=self.key[i]
            ).grid(row=0, column=i, padx=20, pady=20)
            
        week = 1
        for num in range(1, month+1):
            num += offset
            day = Day(num, offset, self.master,  f"{today.month}/{num-offset}/{today.year}", self)
            day.grid(row=week, column=num%7, padx=5, pady=5)
            self.days.append(day)
            if (num+1)%7==0:
                week+=1
        
        if mainloop:
            self.master.mainloop()

class Day(ctk.CTkButton):
    def __init__(self, num: int, offset: int, master: ctk.CTk, fulldate: str, calendar: Calendar) -> None:
        super().__init__(
                master, 
                text=f"{num-offset}",
                height=140,
                font=("Default", 30),
                fg_color=None,
                command=self.open_log
                )
        self.log, self.win = None, None
        self.master = master
        self.logger = master.logger
        self.fulldate = fulldate
        self.calendar = calendar

    def open_log(self):
        self.logger.debug(self.master.logged)
        if self.win:
            if not self.win.winfo_exists():
                for day in self.calendar.days:
                    if day != self and day.win:
                        day.win.destroy()
                self.win = Log(self.master, self.fulldate)
            else:
                self.win.focus()
        else:
            for day in self.calendar.days:
                if day != self and day.win:
                    day.win.destroy()
            self.win = Log(self.master, self.fulldate)
    
class Log(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, title: str) -> None:
        super().__init__(master)
        self.geometry("400x300")
        self.master = master
        self.logger = self.master.logger
        self.date = title
        super(Log, self).title(title)
        self.label = ctk.CTkLabel(self, text=f"Hello?")
        self.label.pack(padx=20, pady=20)

        elements = []
        self.entry = ctk.CTkEntry(
                self,
                placeholder_text=f"Enter name of food"
        )
        self.entry.pack()
        elements.append(self.entry)
        self.entry2 = ctk.CTkEntry(
                self,
                placeholder_text=f"Enter quantity IN GRAMS"
        )
        self.entry2.pack()
        elements.append(self.entry2)

        button = ctk.CTkButton(
            self, 
            text="Submit",
            command=lambda: self.submit(elements)
        )
        button.pack()

        self.transient(self.master)
        
    
    def submit(self, elements: list[ctk.CTkEntry]) -> None:
        self.logger.debug([element.get() for element in elements])
        if self.date not in self.master.logged:
            self.master.logged.append(self.date)
        self.logger.debug(self.master.logged)
        algorithm = Algorithm(elements[0].get(), int(elements[1].get()), self.logger)
        algorithm.run()
        if int(datetime.now().strftime("%m")) != int(self.master.logged[0][0:2]):
            self.master.logged = []
            nutrients = {
                "Protein": [0, "g"],
                "Fat": [0, "g"],
                "Carbs": [0, "g"],
                "Calories": [0, "kcal"],
                "Sugar": [0, "g"],
                "Fiber": [0, "g"],
                "Calcium": [0, "mg"],
                "Iron": [0, "mg"],
                "Potassium": [0, "mg"],
                "Sodium": [0, "mg"],
                "Vitamin C": [0, "mg"],
                "Cholesterol": [0, "mg"]
            }
            with open("json/food.json", "w") as f:
                json.dump(nutrients, f, indent=4)
                print("WHYYYYYYYYY")
            with open("json/food.json", "r") as f:
                print(json.load(f))
        


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Calendar(ctk.CTk())
    app.run()