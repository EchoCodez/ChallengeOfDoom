import customtkinter as ctk
from datetime import datetime
from calendar import monthrange



class CTkCalender:
    def __init__(self, master):
        self.master = master
        self.run()
    
    def run(self, *, font=("Default", 30), color=None, mainloop=True) -> None | list[ctk.CTkButton]:
        today = datetime.today()
        offset, days_in_this_month = monthrange(today.year, today.month)
        # TODO: Make it match up with days of the week using `offset`
        week = 0
        days = []
        for day in range(days_in_this_month):
            day_button = ctk.CTkButton(
                self.master,
                text=f"{day+1}",
                height=140,
                font=font,
                fg_color=color
                )
            day_button.grid(row=week, column=day%7, padx=5, pady=5)
            days.append(day_button)
            day+=1
            if day%7==0:
                week+=1
                
        if mainloop:
            self.master.mainloop()
        else:
            return days

        

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = CTkCalender(ctk.CTk())
