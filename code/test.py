from tkinter import *
import customtkinter as ctk
import json


class RunProgram:
    def __init__(self) -> None:
        self.preferences = "preferences.json"
        self.root = ctk.CTk()
    
    def quit_and_clean(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.quit()
        
        with open(self.preferences, "w") as f:
            ob = json.dumps({"appearance_theme":self.var.get()})
            print(ob)
            f.write(ob)
    
    def set_appearance(self):
        def change():
            label.configure(text=f"You have selected {self.var.get()} mode")
            if self.var.get() == 'dark':
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        
        with open(self.preferences) as f:
            data = json.load(f)
            print(data)
            if data.get("appearance_theme", False):
                ctk.set_appearance_mode(data["appearance_theme"])
                return
        
        self.root.geometry("400x300")
        self.var = StringVar()
        
        question = ctk.CTkLabel(self.root, text="Which appearance theme would you like to use?")
        label = ctk.CTkLabel(self.root, text="You have selected light mode")
        dark_button = ctk.CTkRadioButton(self.root, text="Dark", variable=self.var, value="dark", command=change)
        light_button = ctk.CTkRadioButton(self.root, text="Light", variable=self.var, value="light", command=change)
        next_button = ctk.CTkButton(self.root, text="Next", command=self.quit_and_clean)
        
        question.pack()
        dark_button.pack()
        light_button.pack()
        label.pack()
        next_button.pack()
        
        self.root.mainloop()
    
    def run(self):
        pass
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.mainloop()
        # ctk.CTkButton()


def main(erase_data = False):
    program = RunProgram()\
    
    if erase_data: # only for testing purposes; delete in final push
        with open(program.preferences, "w") as f:
            f.write("{}")
    
    program.set_appearance()
    program.run()
    


if __name__ == "__main__":
    main()