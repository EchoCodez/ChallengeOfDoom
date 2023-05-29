import customtkinter as ctk
from logging import Logger
import sys
sys.path.append("../setup")

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
    
    def submit(self, elements) -> None:
        try:
            for i in range(1, 4):
                int(elements[i].get())
            for i in range(4, 7):
                if int(elements[i].get()[0])*10+int(elements[i].get()[1]) > 12 or int(elements[i].get()[3])*10+int(elements[i].get()[4]) > 60:
                    raise SystemError
                if elements[i].get()[2] != ":":
                    raise SystemError
                if elements[i].get()[6]+elements[i].get()[7] != "AM" and elements[i].get()[6]+elements[i].get()[7] != "PM":
                    raise SystemError
            self.logger.debug([element.get() for element in elements])
            ctk.CTkLabel(
                self.master,
                text="Thanks! Your input has been recieved!"
            ).grid(row=4, column=4, padx=20, pady=20)
        except:
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