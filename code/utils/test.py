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
        week = 0
        for day in range(days_in_this_month):
            ctk.CTkButton(
                self,
                text=f"{day+1}",
                height=140,
            ).grid(row=week, column=day%7, padx=5, pady=5)
            day+=1
            if day%7==0:
                week+=1
        self.mainloop()

        

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
