import customtkinter as ctk

class Tips():
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
    
    def run(self, mainloop: bool = True) -> None:
        self.label = ctk.CTkLabel(self.master, text="aint no way")
        self.label.pack()
        if mainloop:
            self.master.mainloop()