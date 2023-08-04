import re
import tkinter as tk
import customtkinter as ctk
import webbrowser
from datetime import datetime, date
from CTkMessagebox import CTkMessagebox
from logging import Logger
from utils import (
    jsonUtils,
    MCQbuiler,
    CustomQuestion,
    Question,
    set_theme,
    InformationSheet,
    ActionButton,
    UserInfo
)
from api.diagnosis import Diagnosis
from setup.special import InformationPages
from setup.setup import get_information_texts
from api.location import get_location


preferences = "json/preferences.json"
user_data = "json/user-data.json"
conditions_list = "json/symptoms.json"

GENERATOR = (str(i) for i in range(1)).__class__

def _ceil(n: float) -> int:
    return int(n) if isinstance(n, int) or n.is_integer() else int(n)+1

class Questions(ctk.CTk):
    '''Setup questions for application'''
    def __init__(self, logger: Logger, fg: str = None) -> None:
        
        super().__init__(fg_color=fg)
        
        self.__appearance = tk.StringVar(value="light")
        self._selected_conditions: dict[str, tk.BooleanVar] = {}
        self.logger = logger
        self._conditions: GENERATOR = iter(d["Name"] for d in jsonUtils.read(conditions_list))
        self.total_condition_pages = None
    
    def raise_exception(self, mainloop: bool = False, **kwargs) -> CTkMessagebox:
        return CTkMessagebox(self, **kwargs) if not mainloop else CTkMessagebox(self, **kwargs).mainloop()
    
    def on_closing(self) -> None:
        '''Confirm if user wanted to end application'''
        
        self.logger.info("User clicked X button")
        
        answer = self.raise_exception(
            title="Quit?",
            icon="question",
            message="Do you want to close the application?",
            option_1="Cancel",
            option_2="Yes"
            )
        if answer.get() == "Yes":
            self.logger.debug("Exited program")
            self.withdraw()
            return
        else:
            self.logger.info("Canceled exiting program")
    
    def clean(self) -> None:
        '''
        Clean the tkinter window of widgets
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
            CustomQuestion(self.get_year_of_birth),
            CustomQuestion(self.get_contact),
            CustomQuestion(self.get_location),
            include_end=False
        )
        answers = prequiz.begin()
        
        l = get_location(answers[4], self.logger)
        lat, long = l.latitude, l.longitude
        jsonUtils.write({
                "gender": answers[1],
                "location": {"latitude": lat, "longitude": long}
            })
        
        self.clean()
    
    def set_appearance(self) -> None:
        '''Choose dark or light theme for custom tkinter'''
        
        def change() -> None:
            '''Toggle light and dark theme'''
            
            if self.__appearance.get() == 'dark':
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
        
        def cont():
            jsonUtils.write({"appearance_theme":self.__appearance.get()}, file=preferences)
            self.logger.debug(f"Successfully wrote appearance theme {self.__appearance.get()} to file")
            self.quit()
        
        # get user input for choice of theme
        
        question = ctk.CTkLabel(
            self,
            text="Which appearance theme would you like to use?",
            font=("Default", 50)
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
    
    
        question.pack(pady=100)
        dark_button.pack(pady=20)
        light_button.pack(pady=20)
        next_button.pack(pady=50)
        
        self.mainloop()
    
    def _checkboxes(
            self,
            gender: str,
            font: tuple[str, int] = ("Arial", 25),
            rows: int = 15,
            columns: int = 3,
        ) -> None:
        '''Creates the checkboxes
        '''
        
        if gender == "male":
            male = True
        elif gender == "female":
            male = False
        else:
            raise ValueError("Gender must be provided as either male or female")
        
        def new_name():
            '''Filter out options of opposite gender'''
            
            name = next(self._conditions, None)
            
            if name is None:
                return None
            elif male and any(word in name for word in ["vagina", "period"]):
                return new_name()
            elif not male and any(word in name for word in ["testicle"]):
                return new_name()
            else:
                return name
        
        # make column outer loop so that things with long names get grouped into one column, saving space
        for j in range(columns):
            for i in range(1, rows+1):
                name = new_name()
                
                if name is None:
                    return
                
                self._selected_conditions[name]=tk.BooleanVar(value=False)
                checkbox = ctk.CTkCheckBox(
                        self, 
                        text = name,
                        variable = self._selected_conditions[name],
                        onvalue = True,
                        offvalue = False,
                        font = font
                    )
                checkbox.grid(
                    row = i,
                    column = j,
                    pady = 10,
                    padx=40,
                    sticky = tk.W
                )
    
    def get_previous_medical_conditions(self, font="Default") -> None:
        """Create checkboxes of previous medical conditions

        Parameters:
        -----------
            font (str, optional): font options for title and next button. Font size is immutable. Defaults to "Default".
        """ 
        self.clean()
        
        rows, columns = 15, 3
        
        total_names = len(jsonUtils._open(conditions_list))
        
        gender = jsonUtils.read("json/user-data.json").get("gender", "male").lower()
        
        for i in range(_ceil(total_names/(rows*columns))):
            def continue_button():
                self.clean()
                self.quit()
                self.logger.debug(f"Onto page {i+1}")
            
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
            
            self._checkboxes(
                    gender=gender,
                    font=(font, 30),
                    columns=columns,
                    rows=rows
                )
            
            next_button.grid(row=rows+1, column=columns-1, sticky = tk.W, pady=30)
            next_button.lift()
            
            self.mainloop()

    def get_year_of_birth(self, font = ("None", 50)): # CustomQuestion
        def verify_and_continue():
            typed = typer.get().strip()
            year = datetime.now().year
            self.logger.info(f"User typed {typed} as input for date of birth")
            
            birth_year = re.sub("\D", "", typed)
            
            if birth_year == "":
                CTkMessagebox(
                    self,
                    title="Date of Birth Submission Error",
                    message=f"Expected year between 1930 and {year}, but got \"{typed}\"",
                    icon="cancel"
                )
                return
            
            birth_year = int(birth_year)
            self.logger.debug(f"Transformed {typed} to {birth_year}")
            
            if birth_year not in range(1930, year+1):
                self.logger.info(f"User entered date of birth outside 1930 and {year}")
                CTkMessagebox(self, title="Date of Birth Submission Error",message=f"Must be a year between 1930 and {year}", icon="cancel")
            else:
                self.logger.info("User entered valid date of birth")
                jsonUtils.write(
                    data={"birth_year": birth_year}
                )
                self.logger.info(f"Birth year {birth_year} succesfully written to file")
                self.quit()
        
        typer = ctk.CTkEntry(
            self,
            width=400,
            height=400,
            font=("Times New Roman", 25),
            placeholder_text="Type Here"
            )

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
        title.pack(pady=100)
        subtitle.pack(pady=20)
        typer.pack(pady=20)
        next_button.pack(pady=20)
        self.mainloop()

    def get_contact(self, font = ("None", 50)):
        def verify_and_continue():
            contact = typer.get().strip()
            jsonUtils.write(
                data={"contact": contact}
            )
            self.quit()

        typer = ctk.CTkEntry(
            self,
            width=200,
            height=50,
            font=("Times New Roman", 25),
            placeholder_text="Type Here"
            )

        title = ctk.CTkLabel(
            self,
            text="Enter contact information",
            font=font
        )
        
        subtitle = ctk.CTkLabel(
            self,
            text="Enter your email in the format youremail@example.com.",
            font=("", 20)
        )

        subtitle2 = ctk.CTkLabel(
            self,
            text="Note that leaving blank or inputting an invalid adress will result in no emails being sent for notifications.",
            font=("", 20)
        )

        next_button = ctk.CTkButton(
            self,
            text="Next",
            command=verify_and_continue
        )
        title.pack(pady=100)
        subtitle.pack(pady=20)
        subtitle2.pack(pady=5)
        typer.pack(pady=20)
        next_button.pack(pady=20)
        self.mainloop()
        
    def get_location(self) -> str:
        self.quit()
        self.clean()
        
        ctk.CTkLabel(
            self,
            text="Enter your location",
            font=("DEFAULT", 50)
        ).pack(pady=100)
        
        ctk.CTkLabel(
            self,
            text="This is used to find doctors near you",
            font=("DEFAULT", 30)
        ).pack(pady=50)
        
        texts: list[ctk.CTkEntry] = []
        for text in ("City", "State", "Country"):
            texts.append(ctk.CTkEntry(
                self,
                placeholder_text=text,
                width=280,
                height=56
            ))
            texts[-1].pack(pady=20)
            
        ctk.CTkButton(
            self,
            width=280,
            height=56,
            command=self.quit,
            text="Continue"
        ).pack(pady=20)
        
        self.mainloop()
        return " ".join(t.get() for t in texts)

    def show_register_api_pages(self):
        def create_pages() -> tuple[ctk.CTkEntry, ctk.CTkEntry]:
            return sheets.create_pages(
                self,
                font=("DEFAULT", 30),
                text_color="#FFFFFF" if self.cget("bg")=="gray14" else "#000000",
                state="disabled",
                wrap="word"
            )[0]
        
        sheets = InformationPages(self.logger)
        
        for d in get_information_texts():
            buttons, commands = d.pop("buttons", ()), d.pop("commands", ())
            
            if len(buttons) != len(commands):
                raise TypeError("Must be same amount of buttons as commands")
            
            total_buttons = [ActionButton(button, command) for button, command in zip(buttons, commands)]
            sheets+=InformationSheet(
                buttons=total_buttons,
                **d
            )
        sheets+=CustomQuestion(self.enter_api_username_password)
        sheets: InformationPages
        
        self.clean()
        username, password = create_pages()
        
        while True:
            if not username.get() or not password.get():
                self.logger.debug("Null username or null password")
                self.raise_exception(
                    title="No Username/Password Inputted",
                    message="Username/Password cannot be null. Please note if you put an incorrect username/password, we will be unable to get diagnosis results.",
                    icon="warning"
                )
                self.logger.debug("User entered invalid username/password (null value)")
                self.clean()
                username, password = create_pages()
            elif re.sub("[a-zA-Z0-9]", "", username.get()) or re.sub("[a-zA-Z0-9]", "", password.get()):
                self.raise_exception(
                    title="Invalid Characters",
                    message="Username/Password must only contain latin characters",
                    icon="warning"
                )
                self.logger.debug("User entered invalid username/password (non-latin)")
                self.clean()
                username, password = create_pages()
            else:
                break
        
        jsonUtils.add({
            "api_username": username.get(),
            "api_password": password.get()
        })
        self.logger.debug(f"Added Username {username.get()} and password {password.get()}")

    def enter_api_username_password(self):
        self.clean()
        
        ctk.CTkLabel(
            self,
            text="Enter your api username and password"
        ).pack(pady=100)
        
        username = ctk.CTkEntry(
            self,
            placeholder_text="Live Username",
            width=280,
            height=56
        )
        username.pack(pady=20)
        
        password = ctk.CTkEntry(
            self,
            placeholder_text="Live Password",
            width=280,
            height=56
        )
        password.pack(pady=20)
        
        return username, password

class ApiParent:
    '''Class to put UI diagnosis code for APImedic'''
    def __init__(self) -> None:
        super().__init__()
    
    def _diagnose(self) -> None:
        '''Gather diagnosis data and use it to call API'''
        def call_api(user):
            results = Diagnosis(
                user=user,
                logger=self.logger,
                testing=False
                ).make_call()
            
            if results == "":
                self.raise_exception(
                    title="API Token Error",
                    message="An error occured while fetching diagnosis results.\nPlease check username and password",
                    icon="cancel"
                )
                self.logger.debug("Raised API Token Error")
                self.quit()
                self.home()
            
            self.logger.debug("User made daily diagnosis call.")
            
            file = f"json/health/{date.today().strftime('%d_%m_%y')}.json"
            jsonUtils.overwrite(
                data = results,
                file = file
                )
            self.logger.info(f"Writing to log file '{file}' completed successfully")
            
            # writes it to list of logs
            logs: list[str] = jsonUtils._open("json/logs.json")["logs_list"]
            logs+=[file] if file not in logs else []
            logs.sort(key=lambda d: datetime.strptime(d.replace("json/health/", "")[:-5], "%d_%m_%y"))
            jsonUtils.write(
                data={"logs_list": list(logs)},
                file="json/logs.json"
            )
            
            self.logger.info("Added log file name to logs.json")
        
        self.clean()
        
        MCQbuiler(
            self,
            "Daily Checkup",
            self.logger,
            CustomQuestion(self.get_previous_medical_conditions)
        ).begin(
            title_next="Data gathered!",
            continue_text="Diagnose me",
            next_button_width=300,
            next_button_height=70
            )
        
        self.quit()
        
        test_results = [key for key, val in self._selected_conditions.items() if val.get()]
        user = jsonUtils.get_values()
        
        conditions = user.conditions.copy()
        
        for condition in test_results:
            conditions+= [jsonUtils.search(
                conditions_list,
                sentinal=condition,
                search_for="Name",
                _return="ID"
                )]
            
        edited_user = UserInfo(
            conditions,
            user.preferences,
            user.gender,
            user.birthyear,
            user.api_username,
            user.api_password
        )
        
        call_api(user=edited_user)
        self.logger.debug("Finished gathering data")
        
        self._show_diagnosis_results()
        self.home()
     
    def _show_diagnosis_results(self, font: str | tuple[str, int] = ("Times New Roman", 35)) -> None:
        self.clean()
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
        
        
        diseases = jsonUtils.read(date.today().strftime("json/health/%d_%m_%y.json"))
        self.get_diagnosis_info(diseases, tabview, font)
        self.mainloop()
        
    def get_diagnosis_info(self, diseases: str|list[dict], tabview: ctk.CTkTabview, font = ("Times New Roman", 35), loop=False) -> None:
        '''Create tabview with each disease'''
        if isinstance(diseases, str):
            self.logger.error(f"Unable to get diagnosis results: {diseases}")
            
            ctk.CTkLabel(
                tabview,
                text=f"Unable to get diagnosis results: {diseases}"
            ).grid(pady=20)
            ctk.CTkButton(
                self,
                text="Back to Homepage",
                command=self.quit
            ).pack(pady=20)
            self.mainloop()
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
