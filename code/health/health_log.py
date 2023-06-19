from __future__ import annotations

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
    
    def run(self, mainloop: bool = True) -> None:
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
            day = Day(num, offset, self.master, f"{today.month}/{num-offset}/{today.year}")
            day.grid(row=week, column=num%7, padx=5, pady=5)
            days.append(day)
            if (num+1)%7==0:
                week+=1
                
        for day in days:
            day.add_days(*days)
            
        self.logger.debug([element._text for element in days])
        if mainloop:
            self.master.mainloop()

class Day(ctk.CTkButton):
    def __init__(self, num: int, offset: int, master: ctk.CTk, fulldate: str) -> None:      
        super().__init__(
            master, 
            text=f"{num-offset}",
            height=140,
            font=("Default", 30),
            command=self.open_log
        )
        self.log = None
        self.days = None # list of days
        self.fulldate = fulldate

    @property
    def isactive(self):
        return self.log is not None

    def open_log(self):
        '''Open a new window containing information about that date'''
        
        if not self.days:
            raise Exception("Days must be passed in before creating log")
        
        # delete previous day windows so only one log is open at a time
        for day in self.days:
            if day.isactive:
                day.destroy()
        
        # create window
        self.log = Log(self.master, self.fulldate)
    
    def destroy(self):
        '''Destroy log and set `self.log=None`'''
        
        self.log.destroy()
        self.log = None

        
    def add_days(self, *days: Day):
        self.days = days
    
    
class Log(ctk.CTkToplevel):
    def __init__(self, master, title) -> None:
        super().__init__(master,)
        self.geometry("400x300+0+0")
        super(Log, self).title(title)

        self.label = ctk.CTkLabel(self, text=f"")
        self.label.pack(padx=20, pady=20)

        self.transient(self.master)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Calendar(ctk.CTk())
    app.run()