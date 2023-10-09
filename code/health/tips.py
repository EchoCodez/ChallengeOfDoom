import customtkinter as ctk

class Tips():
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
    
    def run(self, mainloop: bool = True) -> None:
        with open ("json/food.json"):
            pass
        if mainloop:
            self.master.mainloop()