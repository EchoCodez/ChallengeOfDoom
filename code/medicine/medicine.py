import customtkinter as ctk
from utils import Notification, constants, Logger
import json

class Medicine:
    def __init__(self, master: ctk.CTk, logger: Logger) -> None:
        self.master = master
        self.logger = logger
        self.labels = {
            0: "Medicine Name",
            1: "Morning", 
            2: "Afternoon", 
            3: "Evening",
            4: "Breakfast Time",
            5: "Lunch Time",
            6: "Dinner Time",
            7: "Before/After Meal",
        }
    
    def submit(self, elements: list) -> None:
        try:
            for i in range(1, 4):
                int(elements[i].get())
            if elements[0] == "":
                raise SystemError
            for i in range(4, 7):
                hours = ""
                for j in elements[i].get():
                    if j == ":":
                        break
                    hours += j
                int(hours)
                if len(hours) != 1:
                    if int(elements[i].get()[0])*10+int(elements[i].get()[1]) > 12:
                        raise ValueError
                    if int(elements[i].get()[3])*10+int(elements[i].get()[4]) > 60:
                        raise ValueError
                    if elements[i].get()[2] != ":":
                        raise ValueError
                    if elements[i].get()[6]+elements[i].get()[7] != "AM" and elements[i].get()[6]+elements[i].get()[7] != "PM":
                        raise ValueError
                else:
                    if int(elements[i].get()[2])*10+int(elements[i].get()[3]) > 60:
                        raise ValueError
                    if elements[i].get()[1] != ":":
                        raise ValueError
                    if elements[i].get()[5]+elements[i].get()[6] != "AM" and elements[i].get()[5]+elements[i].get()[6] != "PM":
                        raise ValueError
            self.logger.debug([element.get() for element in elements])
            data = {}
            for i in range(8):
                data[self.labels[i]] = elements[i].get() 
            print(data)
            with open(constants.MEDICINE, 'r', encoding="utf-8") as f:
                feeds = json.load(f)
            feeds.extend([data])
            with open(constants.MEDICINE, 'w', encoding="utf-8") as f:
                json.dump(feeds, f, indent=4)
            self.master.add_notifs(data)
            self.master.home()

        except Exception as e:
            self.logger.debug(e)
            self.logger.debug("User failed to input correctly")
            ctk.CTkLabel(
                self.master,
                text="Please enter valid input"
            ).grid(row=4, column=4, padx=20, pady=20)
        

    def run(self) -> None:
        elements = []
        for i in range(8):
            ctk.CTkLabel(
                self.master,
                text=self.labels[i]
            ).grid(row=0, column=i, padx=20, pady=20)
        
        entry = ctk.CTkEntry(
            self.master,
            placeholder_text="Enter medicine name"
        )
        entry.grid(row=1, column=0, padx=20, pady=20)
        elements.append(entry)
        
        for i in range(3):
            entry = ctk.CTkEntry(
                self.master,
                placeholder_text="",
                width=30
            )
            entry.grid(row=1, column=i+1, padx=20, pady=20)
            elements.append(entry)
        
        for i in range(3):
            entry = ctk.CTkEntry(
                self.master,
                placeholder_text="hh:mm AM/PM",
            )
            entry.grid(row=1, column=i+4, padx=20, pady=20)
            elements.append(entry)

        menu = ctk.CTkOptionMenu(
            self.master,
            values=["Before", "After"]
        )
        menu.grid(row=1, column=7, padx=20, pady=20)
        elements.append(menu)

        
        ctk.CTkButton(
            self.master, 
            text="Submit",
            command=lambda: self.submit(elements)
        ).grid(row=2, column=4, padx=20, pady=20)

        
        self.master.mainloop()