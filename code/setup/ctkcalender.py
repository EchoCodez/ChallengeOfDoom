import customtkinter as ctk
from datetime import datetime
from calendar import monthrange



class CTkCalender:
    def __init__(self, master):
        self.master = master
        self.run()
    
    def run(self, font=("Default", 30), color=None) -> None:
        today = datetime.today()
        days_in_this_month = monthrange(today.year, today.month)[1]
        week = 1
        # color="#FFFFFF"
        for i in range(7):
            day = week
            for j in range(days_in_this_month//7):
                ctk.CTkButton(
                    self.master,
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
                self.master,
                text=f"{day+i}",
                height=140,
                font=font,
                fg_color=color
            ).grid(row=j+1, column=i, pady=5, padx=5)

        

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = CTkCalender()
