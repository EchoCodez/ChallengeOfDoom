# library imports
import tkinter as tk
import customtkinter as ctk
import sys
import webbrowser
from datetime import date

# file imports
from utils.parse_json import jsonUtils
from CTkMessagebox import CTkMessagebox
from utils.setup import setup_logging
from utils.mcq import MCQbuiler
from utils.data_classes import Question, CustomQuestion
from api.diagnosis import Diagnosis
from log_processes.health_log import SearchForLog, get_previous_month
from utils.config import set_theme, delete_old_diagnosis
from utils.setup_questions import Questions


preferences = "json/preferences.json"
user_data = "json/user-data.json"
conditions_list = "json/symptoms.json"

class Program(ctk.CTk, Questions):
    """The main program that runs the application

    Parameters:
    -----------
        ctk (str): window background color, tuple: (light_color, dark_color) or single color
    """    
    
    def __init__(self, fg = None) -> None:
        '''
        Initilize self and store file names for ease of access
        
        Name mangling is used to ensure root cannot be used outside of class
        '''
        
        ctk.CTk.__init__(
            self=self,
            fg_color=fg
            )
        Questions.__init__(
            self=self,
            true_self=self
        )
        
        self.logger = setup_logging()
        self.title("Congressional App Challenge 2023")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.focus_force()
        
        self.__setup_finished = jsonUtils.open(preferences).get("setup_finished", False)
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
        
    def get_diagnosis_info(self, diseases: str|list[dict], tabview: ctk.CTkTabview, font = ("Times New Roman", 35), loop=False):
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
        
        if loop:
            self.mainloop()
    
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
            
            def show_old_diagnosis(d = _date):
                self.logger.debug(f"Searching for file for date {d}")
                self.clean()
                temp_tabs = ctk.CTkTabview(self)
                temp_tabs.pack()
                self.get_diagnosis_info(
                    SearchForLog(self.logger, date=d).search(),
                    temp_tabs,
                    loop=True
                    )
                self.health_log(font=font)
            
            result = SearchForLog(self.logger, date=_date).search()
            
            if result is None:
                continue
            
            button.configure(
                font=font,
                command=show_old_diagnosis
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
        
        delete_old_diagnosis(self.logger)
        
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
    