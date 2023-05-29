import customtkinter as ctk
from datetime import datetime
from calendar import monthrange

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
    
    def run(self) -> None:
        today = datetime.today()
        offset, month = monthrange(today.year, today.month)
        
        for i in range(7):
            ctk.CTkLabel(
                self.master,
                text=self.key[i]
            ).grid(row=0, column=i, padx=20, pady=20)
            
        week = 1
        days = []
        for num in range(1, month+1):
            num += offset
            day = Day(num, offset, self.master)
            day.grid(row=week, column=num%7, padx=5, pady=5)
            days.append(day)
            if (num+1)%7==0:
                week+=1
        
        print([element._text for element in days])
        self.master.mainloop()

class Day(ctk.CTkButton):
    def __init__(self, num: int, offset: int, master: ctk.CTk) -> None:
        super().__init__(
                master, 
                text=f"{num-offset}",
                height=140,
                font=("Default", 30),
                fg_color=None,
                command=self.open_log
                )
        self.log = None

    def open_log(self):
        win = Log()
    
class Log(ctk.CTkToplevel):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text=f"")
        self.label.pack(padx=20, pady=20)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Calendar(ctk.CTk())
    app.run()