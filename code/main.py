import tkinter as tk
import customtkinter as ctk
import sys
from parse_json import jsonUtils
from CTkMessagebox import CTkMessagebox
from setup import setup_logging
from multiple_choice.mcq import MCQbuiler, Question, CustomQuestion


preferences = "json_files/preferences.json"
user_data = "json_files/user-data.json"
conditions_list = "json_files/symptoms.json"
conditions = "json_files/symptoms.json"

class Program:
    '''Class encompassing all the functions used to run the program'''
    
    def __init__(self, add_attributes = True) -> None:
        '''
        Initilize self.__root and store file names for ease of access
        
        Name mangling is used to ensure root cannot be used outside of class
        
        Parameters:
        -----------
            add_attributes (bool, optional): Add class variables __appearance & __remember
        '''
        
        self.logger = setup_logging()
        self.__root = ctk.CTk()
        self.__root.title("Congressional App Challenge 2023")
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
        width, height = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        self.__root.geometry(f"{width}x{height}+0+0")
        if add_attributes:
            self.__appearance = tk.StringVar(value="light")
            self.__remember = tk.BooleanVar(value=True)
    
    def on_closing(self) -> None:
        '''Confirm if user wanted to end application'''
        self.logger.debug("User clicked X button")
        answer = CTkMessagebox(
            title="Quit?",
            icon="question",
            message="Do you want to close the program?",
            option_1="Cancel",
            option_2="Yes"
            )
        if answer.get() == "Yes":
            self.logger.debug("Exited program")
            sys.exit(0)
        else:
            self.logger.debug("Canceled exiting program")
    
    def clean(self, quit_root=True, destroy=False) -> None:
        '''
        Clean the tkinter window\n
        If quit_root is true, it will also run self.__root.quit()
        '''
        
        for widget in self.__root.winfo_children():
            widget.destroy()
        
        if quit_root:
            self.__root.quit()
        if destroy:
            self.__root.destroy()
        
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
                self.__remember.set(False)
                return
        
        # get user input for choice of theme
        
        # self.__root.geometry("400x300")
        
        question = ctk.CTkLabel(
            self.__root,
            text="Which appearance theme would you like to use?",
            font=("Default", 50)
            )
        label = ctk.CTkLabel(
            self.__root,
            text="You have selected light mode",
            font=("Default", 35),
            )
        
        dark_button = ctk.CTkRadioButton(
            self.__root,
            text="Dark",
            variable=self.__appearance,
            value="dark",
            command=change,
            font=("Default", 25),
            ) 
        light_button = ctk.CTkRadioButton(
            self.__root, 
            text="Light", 
            variable=self.__appearance, 
            value="light", 
            command=change,
            font=("Default", 25),
            )
        next_button = ctk.CTkButton(
            self.__root, 
            text="Next", 
            command=self.clean,
            font=("Default", 25),
            )
        remember_button = ctk.CTkRadioButton(
            self.__root,
            text="Remember my choice", 
            variable=self.__remember, 
            value=True,
            font=("Default", 25),
            )
        dont_remember_button = ctk.CTkRadioButton(
            self.__root,
            text="Don't remember my choice", 
            variable=self.__remember, 
            value=False,
            font=("Default", 25),
            )
    
    
        question.pack(pady=20)
        dark_button.pack(pady=20)
        light_button.pack(pady=20)
        label.pack(pady=20)
        next_button.pack(pady=20)
        remember_button.pack(pady=20)
        dont_remember_button.pack(pady=20)
        
        self.__root.mainloop()
    
    def __checkboxes(self, fontsize: int = 25, font="Arial") -> dict:
        '''Creates the checkboxes
        
        Returns:
        --------
            dict: which conditions were checkmarked
        '''
        
        
        width, height = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        
        conditions = {}
        width_counter = 0
        condition_names = (d["Name"] for d in jsonUtils.open(conditions_list))
        for j in range(100): # choose arbitrarily large value for columns
            checkboxes = []
            widths = 0
            for i in range(2, (height-300)//37): # calculate amount of rows based off of window height
                name = next(condition_names, None)
                if name is None:
                    self.logger.debug("StopIteration")
                    return conditions
                
                conditions[name]=tk.BooleanVar(value=False)
                checkbox = ctk.CTkCheckBox(
                    self.__root, 
                    text=name,
                    variable=conditions[name],
                    onvalue=True,
                    offvalue=False,
                    font=(font, fontsize)
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
            self.logger.debug(widths)
                
            width_counter+=widths
            if width_counter>width:
                self.logger.debug(*(box.cget("text") for box in checkboxes))
                for box in checkboxes:
                    box.destroy()
                return conditions
            
        return conditions
    
    def get_previous_medical_conditions(self, font="Default") -> None:
        """Create checkboxes of previous medical conditions

        Parameters:
        -----------
            font (str, optional): font options for title and next button. Font size is immutable. Defaults to "Default".
        """
        
        def continue_button():
            self.__conditions = {key: value.get() for key, value in self.__conditions.items() if value.get()}
            jsonUtils.add({"conditions": list(self.__conditions.keys())})
            print(jsonUtils.get_values())
            self.clean(quit_root=False)

             
        width, height = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        self.__root.geometry(f"{width}x{height}+0+0")
        title = ctk.CTkLabel(
            self.__root,
            text="Do you have any previous medical conditions from the list?",
            font=(font, 50)
            )
        next_button = ctk.CTkButton(
            self.__root,
            text="Continue",
            command=continue_button,
            width=280,
            height=56,
            font=(font, 40)
            )
        
        title.grid(
            column=0, 
            columnspan=10, 
            padx=5, 
            pady=5,
            sticky=tk.N
            )
        
        self.__conditions = self.__checkboxes(fontsize=30, font=font)
        
        next_button.grid(pady=10)
            
        self.__root.mainloop()

    def __set_color(self, light: str, dark: str):
        appearance = jsonUtils.search(preferences, "appearance_theme", _return="appearance_theme")
        self.logger.debug(appearance)
        return dark if appearance == "dark" else light
        

    def setup(self) -> None:
        """Sets up the multiple choice quiz and appearance theme
        """        
        
        self.set_appearance()
        # TODO: Check if they have already answered the multiple choice quiz
        prequiz = MCQbuiler(
            self.__root,
            "Pre-quiz", # title
            self.logger,
            Question("What is your gender?", ["Male", "Female"]),
            Question("When were you born?", []), # TODO: Make this a CustomQuestion, and make them type it in
            CustomQuestion(self.get_previous_medical_conditions)
        )
        answers = prequiz.begin()
        self.clean(quit_root=False)
    
    def run(self) -> None:
        '''Main function that executes the program'''
        
        
        # ctk.CTkButton(self.__root, text="Break", command=self.__root.quit).pack()
        # self.__root.mainloop()
        self.__set_color("", "")


def main(*, erase_data = False) -> None:
    '''Wrapper for running the program
    
    Parameters
    ----------
    erase_data: bool
        Debugging parameter to erase all data in preferences.json and user-data.json
    '''

    logger = setup_logging()
    program = Program()
    
    if erase_data: # only for testing purposes; delete in final push
        jsonUtils.clearfiles()
    
    program.setup()
    program.run()
    


if __name__ == "__main__":
    main(erase_data=True)
    