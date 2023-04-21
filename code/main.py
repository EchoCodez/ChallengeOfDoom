import tkinter as tk
import customtkinter as ctk
from os.path import dirname
from parse_json import jsonUtils


basedir = dirname(__file__)


preferences = "preferences.json"
user_data = "user-data.json"


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
            self.__root.quit()
            self.__root.destroy()
    
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
        if self.__remember:
            jsonUtils.add({"appearance_theme":self.__appearance.get()}, file=preferences)
            self.__remember = False
    
    def set_appearance(self) -> None:
        '''Choose dark or light theme for custom tkinter'''
        
        def change() -> None:
            '''Toggle light and dark theme'''
            
            label.configure(text=f"You have selected {self.__appearance.get()} mode")
            if self.__appearance.get() == 'dark':
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        
        def swap_bool() -> None:
            self.__remember = not self.__remember
        
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
            value=True, 
            command=swap_bool
            )
        dont_remember_button = ctk.CTkRadioButton(
            self.__root,
            text="Don't remember my choice", 
            variable=self.__remember, 
            value=False, 
            command=swap_bool
            )
    
    
        question.pack()
        dark_button.pack()
        light_button.pack()
        label.pack()
        next_button.pack()
        remember_button.pack()
        dont_remember_button.pack()
        
        self.__root.mainloop()

    def setup(self) -> None:
        self.set_appearance()
        # TODO: Ask user what previous medical conditions they have
    
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
    main(erase_data=True)
    