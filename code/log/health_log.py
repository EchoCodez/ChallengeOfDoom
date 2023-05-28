import customtkinter as ctk
from datetime import datetime
from calendar import monthrange

class Calendar:
    def __init__(self, master):
        self.master = master
    
    @staticmethod
    def get_key(reverse=False):
        key = {
            0: "Sunday",
            1:"Monday",
            2:"Tuesday",
            3:"Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        }
        return key if not reverse else dict((v, k) for k, v in key.items())
    
    @staticmethod
    def num_to_day(__n: int, /):
        return Calendar.get_key()[__n]
    
    @staticmethod
    def day_to_num(__s: str, /):
        return Calendar.get_key(reverse=False)[__s]
    
    def run(self) -> None | list[ctk.CTkButton]:
        today = datetime.today()
        offset, month = monthrange(today.year, today.month)
        
        for i in range(7):
            ctk.CTkLabel(
                self.master,
                text=self.num_to_day(i)
            ).grid(row=0, column=i, padx=20, pady=20)
            
        # Add empty boxes before start of month and at end of month
        week = 1
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
        win = ToplevelWindow()
    
class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

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