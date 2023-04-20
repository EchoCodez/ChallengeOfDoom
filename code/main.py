import tkinter as tk
import customtkinter as ctk
import json
from parse_json import jsonUtils


class RunProgram:
    '''Class encompassing all the functions used to run the program'''
    def __init__(self) -> None:
        '''Initilize class master root and store file names for ease of access'''
        self.preferences = "preferences.json"
        self.user_data = "user-data.json"
        self.root = ctk.CTk()
    
    def quit_and_clean(self):
        '''Clean the tkinter window'''
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.quit()
        
        # write appearance theme preferences to file
        if self.remember:
            with open(self.preferences, "w") as f:
                ob = json.dumps({"appearance_theme":self.var.get()})
                f.write(ob)
            self.remember = False
    
    def set_appearance(self):
        '''Choose dark or light theme for custom tkinter'''
        def change():
            '''Toggle light and dark theme'''
            label.configure(text=f"You have selected {self.var.get()} mode")
            if self.var.get() == 'dark':
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        
        def swap_bool():
            self.remember = not self.remember
        
        # check if theme preference in file already
        with open(self.preferences) as f:
            data = json.load(f)
            if data.get("appearance_theme", False):
                ctk.set_appearance_mode(data["appearance_theme"])
                return
        
        # get user input for choice of theme
        self.root.geometry("400x300")
        self.var = tk.StringVar()
        self.remember = tk.BooleanVar(value=True)
        
        question = ctk.CTkLabel(self.root, text="Which appearance theme would you like to use?")
        label = ctk.CTkLabel(self.root, text="You have selected light mode")
        dark_button = ctk.CTkRadioButton(self.root, text="Dark", variable=self.var, value="dark", command=change)
        light_button = ctk.CTkRadioButton(self.root, text="Light", variable=self.var, value="light", command=change)
        next_button = ctk.CTkButton(self.root, text="Next", command=self.quit_and_clean)
        remember_button = ctk.CTkRadioButton(self.root, text="Remember my choice", variable=self.remember, value=True, command=swap_bool)
        dont_remember_button = ctk.CTkRadioButton(self.root, text="Don't remember my choice", variable=self.remember, value=False, command=swap_bool)
        
        question.pack()
        dark_button.pack()
        light_button.pack()
        label.pack()
        next_button.pack()
        remember_button.pack()
        dont_remember_button.pack()
        
        self.root.mainloop()
    
    def run(self):
        '''Main function that executes everything for the app'''
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.mainloop()
        # ctk.CTkButton()


def main(erase_data = False):
    '''Wrapper for running the program
    
    Parameters
    ----------
    erase_data: bool
        Debugging parameter to erase all data in preferences.json and user_data.json'''
    program = RunProgram()
    
    if erase_data: # only for testing purposes; delete in final push
        jsonUtils.clearfile(program.preferences)
        jsonUtils.clearfile(program.user_data)
    
    program.set_appearance()
    program.run()
    


if __name__ == "__main__":
    main()