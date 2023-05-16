import customtkinter as ctk
from datetime import datetime
from calendar import monthrange

class Calendar():
    def __init__(self, master):
        self.master = master
    
    def run(self) -> None | list[ctk.CTkButton]:
        today = datetime.today()
        offset, month = monthrange(today.year, today.month)
        # TODO: Make it match up with days of the week using `offset`
        week = 0
        days = []
        for num in range(1, month+1):
            num += offset
            day = Day(num, offset, self.master)
            day.grid(row=week, column=num%7, padx=5, pady=5)
            days.append(day)
            if (num+1)%7==0:
                week+=1
        
        print([thing._text for thing in days])
        self.master.mainloop()

class Day(ctk.CTkButton):
    def __init__(self, num, offset, master) -> None:
        super().__init__(
                master, 
                text=f"{num-offset}",
                height=140,
                font=("Default", 30),
                fg_color=None,
                command=lambda: self.open_log()
                )
        self.log = None

    def open_log(self):
        print(self._text)
    

class Log(ctk.CTk):
    def __init__(self) -> None:
        super().__init__(None)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.hi = "what"
    
    def run(self) -> None:
        self.mainloop()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Calendar(ctk.CTk())
    app.run()