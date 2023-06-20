import customtkinter as ctk
from datetime import datetime
from calendar import monthrange
from logging import Logger

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
        
        self.logger.debug([element._text for element in self.days])
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
        self.log, self.win = None
        self.fulldate = fulldate
        self.calendar = calendar

    def open_log(self):
        for day in self.calendar.days:
            if day != self and day.win:
                day.win.destroy()
        self.win = Log(self.master, self.fulldate)
    
class Log(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, title: str) -> None:
        super().__init__(master)
        self.geometry("400x300")
        super(Log, self).title(title)
        self.label = ctk.CTkLabel(self, text=f"")
        self.label.pack(padx=20, pady=20)

        self.transient(self.master)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Calendar(ctk.CTk())
    app.run()