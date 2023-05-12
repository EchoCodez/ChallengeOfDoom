# library imports
import tkinter as tk
import customtkinter as ctk
import sys
import webbrowser
import re
from datetime import datetime, date

# file imports
from utils.parse_json import jsonUtils
from CTkMessagebox import CTkMessagebox
from utils.setup import setup_logging
from utils.mcq import MCQbuiler
from utils.data_classes import Question, CustomQuestion
from api.diagnosis import Diagnosis
from log_processes.health_log import GetLogs, SearchForLog, get_previous_month
from utils.config import set_theme


preferences = "json/preferences.json"
user_data = "json/user-data.json"
conditions_list = "json/symptoms.json"

class Program(ctk.CTk):
    """The main program that runs the application

    Parameters:
    -----------
        ctk (str): window background color, tuple: (light_color, dark_color) or single color
    """    
    
    def __init__(self, ctk = None) -> None:
        '''
        Initilize self and store file names for ease of access
        
        Name mangling is used to ensure root cannot be used outside of class
        '''
        
        super().__init__(fg_color=ctk)
        
        self.logger = setup_logging()
        self.title("Congressional App Challenge 2023")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.focus_force()
        
        self.__setup_finished = jsonUtils.open(preferences).get("setup_finished", False)
        self.__appearance = tk.StringVar(value="light")
        self.resizable(width=True, height=True)
    
    def on_closing(self) -> None:
        '''Confirm if user wanted to end application'''
        
        self.logger.info("User clicked X button")
        
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
    
    def clean(self) -> None:
        '''
        Clean the tkinter window of widgets\n
        If quit_root is true, it will also run self.quit()
        '''
        
        for widget in self.winfo_children():
            widget.destroy()
        
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
            self.quit()
        
        # get user input for choice of theme
        
        question = ctk.CTkLabel(
            self,
            text="Which appearance theme would you like to use?",
            font=("Default", 50)
            )
        label = ctk.CTkLabel(
            self,
            text="You have selected light mode",
            font=("Default", 35),
            )
        
        dark_button = ctk.CTkRadioButton(
            self,
            text="Dark",
            variable=self.__appearance,
            value="dark",
            command=change,
            font=("Default", 25),
            ) 
        light_button = ctk.CTkRadioButton(
            self, 
            text="Light", 
            variable=self.__appearance, 
            value="light", 
            command=change,
            font=("Default", 25),
            )
        next_button = ctk.CTkButton(
            self, 
            text="Next", 
            command=cont,
            font=("Default", 25),
            )
    
    
        question.pack(pady=20)
        dark_button.pack(pady=20)
        light_button.pack(pady=20)
        label.pack(pady=20)
        next_button.pack(pady=20)
        
        self.mainloop()
    
    def __checkboxes(self, fontsize: int = 25, font="Arial") -> dict:
        '''Creates the checkboxes
        
        Returns:
        --------
            dict: which conditions were checkmarked
        '''
        
        
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        
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
                    self, 
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
                    padx=40,
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
    
    def get_previous_medical_conditions(self, font="Default", file="json/conditions.json") -> None: # CustomQuestion
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
            self.quit()

             
        title = ctk.CTkLabel(
            self,
            text="Are you experiencing any of the above from this list?",
            font=(font, 50)
            )
        next_button = ctk.CTkButton(
            self,
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
            pady=20,
            sticky=tk.N
            )
        
        self.__conditions = self.__checkboxes(fontsize=30, font=font)
        
        next_button.place(relx=0.82, rely=0.8, anchor=tk.CENTER)
            
        self.mainloop()       

    def get_year_of_birth(self, font = ("None", 50)): # CustomQuestion
        def verify_and_continue():
            typed = typer.get(1.0, tk.END).strip()
            year = datetime.now().year
            self.logger.info(f"User typed {typed} as input for date of birth")
            
            birth_year = int(re.sub("\D", "", typed))
            self.logger.debug(f"Transformed {typed} to {birth_year}")
            
            if int(birth_year) not in range(1930, year+1):
                self.logger.info(f"User entered date of birth outside 1930 and {year}")
                CTkMessagebox(self, title="Date of Birth Submission Error",message=f"Must be a year between 1930 and {year}", icon="cancel")
            else:
                self.logger.info("User entered valid date of birth")
                jsonUtils.add(
                    data={"birth_year": typed}
                )
                self.logger.info(f"Birth year ::{typed}:: succesfully written to file")
                self.quit()
        
        typer = ctk.CTkTextbox(self, width=400, font=("Times New Roman", 25))
        typer.insert(tk.END, "Type Here")
        
        title = ctk.CTkLabel(
            self,
            text="What year were you born?",
            font=font
            )
        subtitle = ctk.CTkLabel(
            self,
            text="All non-numbers will be ignored",
            font=("", 20)
        )
        next_button = ctk.CTkButton(
            self,
            text="Next",
            command=verify_and_continue
        )
        title.pack(pady=20)
        subtitle.pack(pady=20)
        typer.pack(pady=20)
        next_button.pack(pady=20)
        self.mainloop()

    def setup(self) -> None:
        """Sets up the multiple choice quiz and appearance theme
        """        
        
        prequiz = MCQbuiler(
            self,
            "Let's set up the program!", # title
            self.logger,
            CustomQuestion(self.set_appearance if not set_theme() else lambda: None),
            Question("What is your gender?", ["Male", "Female"]),
            CustomQuestion(self.get_year_of_birth)
        )
        answers = prequiz.begin()
        
        jsonUtils.add({
                "gender": answers[1],
            })
        
        self.clean()
        jsonUtils.add({"setup_finished": True}, file=preferences)
        self.logger.debug(jsonUtils.get_values())
    
    def _diagnose(self):
        def call_api(user):
            results = Diagnosis(user=user).make_call()
            
            self.logger.debug("User made daily diagnosis call.")
            file = f"json/logs/{date.today().strftime('%d_%m_%y')}.json"
            jsonUtils.overwrite(
                data = results,
                file = file
                )
            self.logger.info(f"Writing to log file '{file}' completed successfully")
            
            # writes it to list of logs
            logs = set(jsonUtils.open("json/logs.json")["logs_list"]).union((file,))
            jsonUtils.add(
                data={"logs_list": list(logs)},
                file="json/logs.json"
            )
            
            self.logger.info("Added log file name to logs.json")
        
        self.clean()
        
        MCQbuiler(
            self,
            "Daily Checkup",
            self.logger,
            CustomQuestion(self.get_previous_medical_conditions, kwargs={"file": "json/conditions.json"})
        ).begin()
        
        self.quit()
        
        loading = ctk.CTkLabel(
            self,
            text="Saving results to health log", # TODO
            font=("Times New Roman", 50)
        )
        loading.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        test_results = jsonUtils.read("json/conditions.json")
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
        
        self._show_diagnosis_results()
        self.home()
    
    def _show_diagnosis_results(self, font: str | tuple[str, int] = ("Times New Roman", 35)):
        ctk.CTkLabel(
            self,
            text="Diagnosis results",
            font=(font[0], font[1]+5) if isinstance(font, (tuple, list)) else (font, 40)
        ).pack(pady=20)
        tabview = ctk.CTkTabview(
            self,
            width=600,
            height=500
        )
        tabview.pack(padx=20, pady=20)
        
        
        diseases = jsonUtils.read("json/possible_diseases.json")
        self.get_diagnosis_info(diseases, tabview, font)
        self.mainloop()
        
    def get_diagnosis_info(self, diseases: str|list[dict], tabview: ctk.CTkTabview, font = ("Times New Roman", 35)):
        if isinstance(diseases, str):
            self.logger.error(f"Unable to get diagnosis results: {diseases}")
            ctk.CTkButton(
                self,
                text="Back to Homepage",
                command=self.quit
            )
            return
        
        for disease in diseases:
            issue, specialization = disease["Issue"], disease["Specialisation"]
            name, accuracy = issue["Name"], issue["Accuracy"]
            
            tab = tabview.add(name)
            label = ctk.CTkLabel(
                tab,
                text=f"Name:\n{name}\n\nAccuracy rating:\n{round(accuracy, 2)}%\n\nSee doctors specialized in:\n{', '.join(x['Name'] for x in specialization)}",
                font=font
            )
            label.pack()
        
            ctk.CTkButton(
                tab,
                text="What is this?",
                command=lambda name=name: webbrowser.open_new_tab(f"https://www.google.com/search?q={name.replace(' ', '%20')}")
            ).pack(pady=50)
        
        ctk.CTkButton(
            self,
            text="Back to homepage",
            command=self.quit
        ).pack()
    
    def health_log(self, font=("Times New Roman", 15)):
        self.clean()
        self.logger.debug("Health log accessed")
        tabview = ctk.CTkTabview(
            self,
            width=900,
            height=750,
        )
        tabview.pack(padx=20, pady=20)
        
        tab1 = tabview.add("Diagnosis Log") # Create master for each tab
        
        frame = ctk.CTkScrollableFrame(
            tab1,
            width=900,
            height=750
        )
        frame.pack()
        for button, _date in get_previous_month(frame):
            _date = _date.strftime("%d/%m/%y")
            button.configure(
                font=font,
                command=lambda _date=_date: self.logger.info(SearchForLog(self.logger, date=_date).search())
                )
            button.pack(pady=5)
        
        tab2 = tabview.add("Diet log")
        # Whatever you do here, to make it appear under the tab, make its master `frame`
            
        ctk.CTkButton(
            self,
            text="Back to Homepage",
            command=self.quit
        ).pack()
        self.mainloop()
        self.clean()
        self.home()
    
    def home(self) -> None:
        '''Main function that executes the program'''
        self.logger.debug("Reached Home Screen")
        self.clean()
        
        ctk.CTkButton( # top left
            self,
            fg_color="#ADD8E6",
            text="TBD",
            command=lambda: self.logger.debug("Button Clicked"),
            corner_radius=40,
            height=self.winfo_screenheight()*0.55,
            width=self.winfo_screenwidth()*0.2,
            font=("Times New Roman", 30),
            text_color="#000000",
            ).place(relx=0.15, rely=0.3, anchor=tk.CENTER)
        
        ctk.CTkButton( # bottom right
            self,
            text="Daily Diagnosis",
            command=self._diagnose,
            fg_color="#ADD8E6",
            height=self.winfo_screenheight()*0.55,
            width=self.winfo_screenwidth()*0.2,
            text_color="#000000",
            font=("Times New Roman", 30),
            corner_radius=40
            ).place(relx=0.85, rely=0.6, anchor=tk.CENTER)
        
        ctk.CTkButton( # bottom left
            self,
            fg_color="#ADD8E6",
            text="TBD",
            command=lambda: self.logger.debug("Button Clicked"),
            corner_radius=40,
            height=self.winfo_screenheight()*0.25,
            width=self.winfo_screenwidth()*0.2,
            font=("Times New Roman", 30),
            text_color="#000000",
            ).place(relx=0.15, rely=0.75, anchor=tk.CENTER)
        ctk.CTkButton( # top right
            self,
            text="Health Log",
            fg_color="#ADD8E6",
            command=self.health_log,
            corner_radius=40,
            height=self.winfo_screenheight()*0.25,
            width=self.winfo_screenwidth()*0.2,
            font=("Times New Roman", 30),
            text_color="#000000",
            ).place(relx=0.85, rely=0.15, anchor=tk.CENTER)
        
        self.mainloop()
    
    def execute(self):
        if not self.__setup_finished:
            self.setup()
        else:
            set_theme()
        
        self.logger.info("Attempting to save memory by deleting last months checkup results")
        
        current_date = date.today()
        current_month = current_date.month
        last_month = current_month - 1 if current_month != 1 else 12  
        today_a_month_ago = date(current_date.year, last_month, current_date.day).strftime("%d_%m_%y")
        
        last_months_checkup = f"json/logs/{today_a_month_ago}.json"
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
    