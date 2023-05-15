import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from calendar import monthrange



class App(ctk.CTk):
    def __init__(self, fg_color = None):
        super().__init__(fg_color=fg_color)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.run()
    
    def run(self, font=("Default", 30), color=None):
        today = datetime.today()
        days_in_this_month = monthrange(today.year, today.month)[1]
        week = 1
        # color="#FFFFFF"
        for i in range(7):
            day = week
            for j in range(days_in_this_month//7):
                ctk.CTkButton(
                    self,
                    text=f"{day}",
                    height=140,
                    font=font,
                    fg_color=color
                ).grid(row=j, column=i, pady=5, padx=5)
                day+=7
            week+=1
        
        day-=6
        for i in range(days_in_this_month-day):
            ctk.CTkButton(
                self,
                text=f"{day+i}",
                height=140,
                font=font,
                fg_color=color
            ).grid(row=j+1, column=i, pady=5, padx=5)
        self.mainloop()

        

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
