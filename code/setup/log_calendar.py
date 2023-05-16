import customtkinter as ctk
from datetime import datetime
from calendar import monthrange

class Calendar:
    def __init__(self, master):
        self.master = master
    
    def open_log(self, text):
        print(text)
    
    @staticmethod
    def num_to_day(__n: int, /):
        key = {
            0: "Sunday",
            1:"Monday",
            2:"Tuesday",
            3:"Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        }
        return key[__n]
        
    def run(self) -> None | list[ctk.CTkButton]:
        today = datetime.today()
        offset, month = monthrange(today.year, today.month)
        # TODO: Make empty boxes show
        for i in range(7):
            ctk.CTkLabel(
                self.master,
                text=self.num_to_day(i)
            ).grid(row=0, column=i, padx=20, pady=20)
            
        week = 1
        days = []
        for num in range(1, month+1):
            num += offset # doesn't work... try using last month as example
            day = ctk.CTkButton(
                self.master,
                text=f"{num-offset}",
                height=140,
                font=("Default", 30),
                fg_color=None,
                command=lambda: self.open_log(num-offset)
                )
            day.grid(row=week, column=num%7, padx=5, pady=5)
            days.append(day)
            if (num+1)%7==0:
                week+=1
        
        print([thing._text for thing in days])
        self.master.mainloop()

        
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Calendar(ctk.CTk())
    app.run()
