import tkinter as tk
import customtkinter as ctk
import sys
from os.path import dirname
from parse_json import jsonUtils


basedir = dirname(__file__)


preferences = "preferences.json"
user_data = "user-data.json"
conditions_list = "conditions.json" # https://github.com/Shivanshu-Gupta/web-scrapers/blob/master/medical_ner/medicinenet-diseases.json


class Program:
    '''Class encompassing all the functions used to run the program'''
    def __init__(self) -> None:
        '''
        Initilize self.__root and store file names for ease of access
        Name mangling is used to ensure root cannot be used outside of class
        '''
        
        self.__root = ctk.CTk()
        self.__root.title("Congressional App Challenge 2023")
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self) -> None:
        '''Confirm if user wanted to end application'''
        
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            sys.exit(0)
    
    def clean(self, quit_root=True) -> None:
        '''
        Clean the tkinter window\n
        If quit_root is true, it will also run self.__root.quit()
        '''
        
        for widget in self.__root.winfo_children():
            widget.destroy()
        
        if quit_root:
            self.__root.quit()
        
        # write appearance theme preferences to file
        if self.__remember.get():
            jsonUtils.add({"appearance_theme":self.__appearance.get()}, file=preferences)
            self.__remember = tk.BooleanVar(value=False)
    
    def set_appearance(self) -> None:
        '''Choose dark or light theme for custom tkinter'''
        
        def change() -> None:
            '''Toggle light and dark theme'''
            
            label.configure(text=f"You have selected {self.__appearance.get()} mode")
            if self.__appearance.get() == 'dark':
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        
        # check if theme preference in file already
        with open(preferences) as f:
            if jsonUtils.get(f, "appearance_theme", func = ctk.set_appearance_mode):
                return
        
        # get user input for choice of theme
        
        self.__root.geometry("400x300")
        self.__appearance = tk.StringVar()
        self.__remember = tk.BooleanVar(value=True)
        
        question = ctk.CTkLabel(self.__root, text="Which appearance theme would you like to use?")
        label = ctk.CTkLabel(self.__root, text="You have selected light mode")
        
        dark_button = ctk.CTkRadioButton(
            self.__root,
            text="Dark",
            variable=self.__appearance,
            value="dark",
            command=change
            ) 
        light_button = ctk.CTkRadioButton(
            self.__root, 
            text="Light", 
            variable=self.__appearance, 
            value="light", 
            command=change
            )
        next_button = ctk.CTkButton(
            self.__root, 
            text="Next", 
            command=self.clean
            )
        remember_button = ctk.CTkRadioButton(
            self.__root,
            text="Remember my choice", 
            variable=self.__remember, 
            value=True
            )
        dont_remember_button = ctk.CTkRadioButton(
            self.__root,
            text="Don't remember my choice", 
            variable=self.__remember, 
            value=False
            )
    
    
        question.pack()
        dark_button.pack()
        light_button.pack()
        label.pack()
        next_button.pack()
        remember_button.pack()
        dont_remember_button.pack()
        
        self.__root.mainloop()
    
    def __checkboxes(self) -> dict:
        '''Creates the checkboxes'''
        width, height = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        print("Winwidth=", width)
        conditions = {}
        width_counter = 0
        condition_names = (d["disease"] for d in jsonUtils.open(conditions_list))
        for j in range(100): # choose arbitrarily large value
            checkboxes = []
            widths = 0
            for i in range(2, (height-30)//37):
                name = next(condition_names, None)
                if name is None:
                    print("StopIteration")
                    return conditions
                
                conditions[name]=tk.BooleanVar(value=False)
                checkbox = ctk.CTkCheckBox(
                    self.__root, 
                    text=name,
                    variable=conditions[name],
                    onvalue=True,
                    offvalue=False,
                    font=("Arial", 15)
                    )
                checkbox.grid(
                    row=i, 
                    column=j, 
                    pady=5, 
                    padx=20,
                    sticky=tk.W
                    )
                
                checkbox.update_idletasks() # update the widget size
                widths = max(widths, checkbox.winfo_width()) # height is always 24
                checkboxes.append(checkbox)
            print(widths)
                
            width_counter+=widths
            if width_counter>width:
                print("width: ", width_counter)
                print(*(box.cget("text") for box in checkboxes))
                for box in checkboxes:
                    box.destroy()
                return conditions
            
        return conditions
    
    def get_previous_medical_conditions(self) -> None:
        def continue_button():
            conditions = {key: value.get() for key, value in conditions.items()}
            print(conditions)
            self.clean(quit_root=False)
            
        width, height = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        self.__root.geometry(f"{width}x{height}+0+0")
        title = ctk.CTkLabel(
            self.__root,
            text="What previous medical conditions do you have?",
            font=("Default", 50)
            )
        next_button = ctk.CTkButton(
            self.__root,
            text="Continue",
            command=continue_button
            )
        title.grid(
            column=0, 
            columnspan=10, 
            padx=5, 
            pady=5,
            sticky=tk.E
            )
        
        conditions = self.__checkboxes()
        
        next_button.grid(pady=5)
            
        self.__root.mainloop()

    def setup(self) -> None:
        self.set_appearance()
        self.get_previous_medical_conditions()
    
    def run(self) -> None:
        '''Main function that executes the program'''
        self.__root.geometry(f"{self.__root.winfo_screenwidth()}x{self.__root.winfo_screenheight()}+0+0")
        self.__root.mainloop()


def main(*, erase_data = False) -> None:
    '''Wrapper for running the program
    
    Parameters
    ----------
    erase_data: bool
        Debugging parameter to erase all data in preferences.json and user-data.json'''
        
    program = Program()
    
    if erase_data: # only for testing purposes; delete in final push
        jsonUtils.clearfiles()
    
    program.setup()
    program.run()
    


if __name__ == "__main__":
    main(erase_data=False)
    