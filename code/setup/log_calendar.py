import customtkinter as ctk
from datetime import datetime
from calendar import monthrange

class Calendar:
    def __init__(self, master):
        self.master = master
    
    def open_log(self, text):
        print(text)
    
    def run(self) -> None | list[ctk.CTkButton]:
        today = datetime.today()
        offset, month = monthrange(today.year, today.month)
        # TODO: Make it match up with days of the week using `offset`
        week = 0
        days = []
        for num in range(1, month+1):
            num += offset
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
