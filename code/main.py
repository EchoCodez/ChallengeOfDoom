# library imports
import tkinter as tk
import customtkinter as ctk
import sys
from datetime import datetime, date

# file imports
from utils.parse_json import jsonUtils
from CTkMessagebox import CTkMessagebox
from utils.setup import setup_logging
from utils.mcq import MCQbuiler
from utils.data_classes import Question, CustomQuestion, UserInfo
from api.diagnosis import Diagnosis


preferences = "json_files/preferences.json"
user_data = "json_files/user-data.json"
conditions_list = "json_files/symptoms.json"

class Program:
    '''Class encompassing all the functions used to run the program'''
    
    def __init__(self) -> None:
        '''
        Initilize self.__root and store file names for ease of access
        
        Name mangling is used to ensure root cannot be used outside of class
        '''
        
        self.logger = setup_logging()
        self.__root = ctk.CTk()
        self.__root.title("Congressional App Challenge 2023")
        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.width, self.height = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        self.__root.geometry(f"{self.width}x{self.height}+0+0")
        
        self.__setup_quiz = False
        self.__setup_finished = jsonUtils.open(preferences).get("setup_finished", False)
        self.__appearance = tk.StringVar(value="light")
        self.__remember = tk.BooleanVar(value=True)
    
    def on_closing(self) -> None:
        '''Confirm if user wanted to end application'''
        
        self.logger.info("User clicked X button")
        
        if self.__setup_quiz:
            force_quit = CTkMessagebox(
                title="Unsuccessful Quit",
                icon="cancel",
                message=
                "Sorry, you cannot exit the application until you finish the setup quiz.\
                    \nForcing a shutdown may result in the application no longer working the next time you open it.",
                option_1="Force Quit",
                option_2="Understood"
            )
            if force_quit.get() == "Force Quit":
                self.logger.warning("User chose to force application to shut down")
                sys.exit(0)
            self.logger.debug("User choose to continue with the setup quiz")
            return
        else:
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
            self.logger.info("Canceled exiting program")
    
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
    
    def _appearance_is_set(self) -> bool:
        '''check if theme preference in file already. If it is, update current'''
        with open(preferences) as f:
            if jsonUtils.get(f, "appearance_theme", func = ctk.set_appearance_mode):
                self.__remember.set(False)
                return True
        return False
        
    def set_appearance(self) -> None:
        '''Choose dark or light theme for custom tkinter'''
        
        def change() -> None:
            '''Toggle light and dark theme'''
            
            label.configure(text=f"You have selected {self.__appearance.get()} mode")
            if self.__appearance.get() == 'dark':
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        
        def cont():
            jsonUtils.add({"appearance_theme":self.__appearance.get()}, file=preferences)
            self.clean(quit_root=True)
        
        # get user input for choice of theme
        
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
            command=cont,
            font=("Default", 25),
            )
    
    
        question.pack(pady=20)
        dark_button.pack(pady=20)
        light_button.pack(pady=20)
        label.pack(pady=20)
        next_button.pack(pady=20)
        
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
                
            width_counter+=widths
            if width_counter>width:
                self.logger.debug(*(box.cget("text") for box in checkboxes))
                for box in checkboxes:
                    box.destroy()
                return conditions
            
        return conditions
    
    def get_previous_medical_conditions(self, font="Default", file="json_files/conditions.json") -> None: # CustomQuestion
        """Create checkboxes of previous medical conditions

        Parameters:
        -----------
            font (str, optional): font options for title and next button. Font size is immutable. Defaults to "Default".
        """
        
        def continue_button():
            self.__conditions = {key: value.get() for key, value in self.__conditions.items() if value.get()}
            jsonUtils.overwrite(
                {"conditions": list(self.__conditions.keys())},
                file=file
                )
            self.clean(quit_root=True)

             
        title = ctk.CTkLabel(
            self.__root,
            text="Are you experiencing any of the above from this list?",
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

    def get_year_of_birth(self, font = ("None", 50)): # CustomQuestion
        def verify_and_continue():
            typed = typer.get(1.0, tk.END).strip()
            year = datetime.now().year
            self.logger.info(f"User typed {typed} as input for date of birth")
            
            if not typed.isnumeric():
                self.logger.info("User entered a non numeric string")
                CTkMessagebox(self.__root, title="Date of Birth Submission Error",message="Must be a number", icon="cancel")
            elif int(typed) not in range(1930, year+1):
                self.logger.info(f"User entered date of birth outside 1930 and {year}")
                CTkMessagebox(self.__root, title="Date of Birth Submission Error",message=f"Must be a year between 1930 and {year}", icon="cancel")
            else:
                self.logger.info("User entered valid date of birth")
                jsonUtils.add(
                    data={"birth_year": typed}
                )
                self.logger.info(f"Birth year ::{typed}:: succesfully written to file")
                self.__root.quit()
        
        typer = ctk.CTkTextbox(self.__root, width=400, font=("Times New Roman", 25))
        typer.insert(tk.END, "Type Here")
        
        title = ctk.CTkLabel(
            self.__root,
            text="What year were you born?",
            font=font
            )
        next_button = ctk.CTkButton(
            self.__root,
            text="Next",
            command=verify_and_continue
        )
        title.pack(pady=10)
        typer.pack(pady=10)
        next_button.pack(pady=10)
        self.__root.mainloop()

    def setup(self) -> None:
        """Sets up the multiple choice quiz and appearance theme
        """        
        
        prequiz = MCQbuiler(
            self.__root,
            "Let's set up the program!", # title
            self.logger,
            CustomQuestion(self.set_appearance if not self._appearance_is_set() else lambda: None),
            Question("What is your gender?", ["Male", "Female"]),
            CustomQuestion(self.get_year_of_birth)
        )
        self.__setup_quiz = True
        answers = prequiz.begin()
        
        jsonUtils.add({
                "gender": answers[1],
            })
        
        self.clean(quit_root=False)
        self.__setup_quiz = False
        jsonUtils.add({"setup_finished": True}, file=preferences)
        self.logger.debug(jsonUtils.get_values())
    
    def _diagnose(self):
        def call_api(user):
            results = Diagnosis(user=user).make_call()
            
            self.logger.info("User made daily diagnosis call.")
            file = f"json_files/logs/{date.today().strftime('%d_%m_%y')}.json"
            jsonUtils.overwrite(
                data = results,
                file = file
                )
            self.logger.info(f"Writing to log file '{file}' completed successfully")
            
            # writes it to list of logs
            logs = set(jsonUtils.open("json_files/logs.json")["logs_list"]).union((file,))
            jsonUtils.add(
                data={"logs_list": list(logs)},
                file="json_files/logs.json"
            )
            
            self.logger.info("Added log file name to logs.json")
        
        self.clean(quit_root=False)
        
        MCQbuiler(
            self.__root,
            "Daily Checkup",
            self.logger,
            CustomQuestion(self.get_previous_medical_conditions, kwargs={"file": "json_files/conditions.json"})
        ).begin()
        
        self.clean()
        
        loading = ctk.CTkLabel(
            self.__root,
            text="Saving results to health log", # TODO
            font=("Times New Roman", 50)
        )
        loading.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        test_results = jsonUtils.read("json_files/conditions.json")
        user = jsonUtils.get_values()
        
        for condition in test_results["conditions"]:
            user.conditions+= [jsonUtils.search(
                conditions_list,
                sentinal=condition,
                search_for="Name",
                _return="ID"
                )]
        call_api(user=user)
        
        loading.destroy()
        
        self.home()     
    
    def home(self) -> None:
        '''Main function that executes the program'''
        
        # Frames
        ctk.CTkFrame( # top left
            self.__root,
            fg_color="#ADD8E6",
            corner_radius=40,
            height=self.height*0.55,
            width=self.width*0.2
            ).place(relx=0.15, rely=0.3, anchor=tk.CENTER)
        ctk.CTkFrame( # bottom right
            self.__root,
            fg_color="#ADD8E6",
            corner_radius=40,
            height=self.height*0.55,
            width=self.width*0.2
            ).place(relx=0.85, rely=0.6, anchor=tk.CENTER)
        ctk.CTkFrame( # bottom left
            self.__root,
            fg_color="#ADD8E6",
            corner_radius=40,
            height=self.height*0.25,
            width=self.width*0.2
            ).place(relx=0.15, rely=0.75, anchor=tk.CENTER)
        ctk.CTkFrame( # top right
            self.__root,
            fg_color="#ADD8E6",
            corner_radius=40,
            height=self.height*0.25,
            width=self.width*0.2
            ).place(relx=0.85, rely=0.15, anchor=tk.CENTER)
        
        # Buttons
        ctk.CTkButton(
            self.__root,
            text="Daily Diagnosis",
            command=self._diagnose
            ).place(relx=0.85, rely=0.6, anchor=tk.CENTER)
        self.__root.mainloop()
    
    def execute(self):
        if not self.__setup_finished:
            self.setup()
        else:
            self._appearance_is_set()
        
        logs = jsonUtils.open("json_files/logs.json")["logs_list"]
        
        self.logger.info("Attempting to save memory by deleting last months checkup results")
        
        current_date = date.today()
        current_month = current_date.month
        last_month = current_month - 1 if current_month != 1 else 12  
        today_a_month_ago = date(current_date.year, last_month, current_date.day).strftime("%d_%m_%y")
        
        last_months_checkup = f"json_files/logs/{today_a_month_ago}.json"
        try:
            jsonUtils.delete_file(last_months_checkup)
        except FileNotFoundError:
            self.logger.info(f"Last months checkup was not found. AKA file path {last_months_checkup} was not found.")
        else:
            self.logger.info("Deletion of last months diagnosis was successfull")
            
        self.home()


def main(*, erase_data = False) -> None:
    '''Wrapper for running the program
    
    Parameters
    ----------
    erase_data: bool
        Debugging parameter to erase all data in preferences.json and user-data.json
    '''

    if erase_data: # only for testing purposes; delete in final push
        jsonUtils.clearfiles()

    program = Program()
    
    program.execute()
    


if __name__ == "__main__":
    main(erase_data=False)
    