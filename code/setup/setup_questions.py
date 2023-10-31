import itertools
import re, os, json
import webbrowser
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from typing import Callable, Iterator, Iterable

from api import Diagnosis, get_location
from setup.special import InformationPages
from utils import *


class Questions(ctk.CTk):
    '''Setup questions for application'''
    def __init__(self, fg: str | None = None) -> None:
        super().__init__(fg_color=fg)
        
        self.__appearance = tk.StringVar(value="light")
        self._selected_conditions: dict[str, tk.BooleanVar] = {}
        self.logger = constants.LOGGER
        self.total_condition_pages = None
    
    def raise_exception(self, mainloop: bool = False, **kwargs) -> CTkMessagebox:
        return CTkMessagebox(self, **kwargs) if not mainloop else CTkMessagebox(self, **kwargs).mainloop() # type: ignore
    
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
            with open("json/logged.json", "w") as f:
                json.dump(self.logged, f, indent=4,)
            os._exit(0)
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
            CustomQuestion(self.set_appearance if not set_theme() else lambda: None),
            Question("What is your gender?", ["Male", "Female"]),
            CustomQuestion(self.get_year_of_birth),
            CustomQuestion(self.get_contact),
            include_end=False
        )
        answers = prequiz.begin()
        
        l = get_location(answers[4], self.logger)
        try:
            lat, long = l.latitude, l.longitude # type: ignore
        except AttributeError:
            self.logger.warning("Failed to get location")
        else:
            jsonUtils.write({
                "location": {"latitude": lat, "longitude": long}
            })
        jsonUtils.write({
            "gender": answers[1],
        })
        
        jsonUtils.write({
            "api_username": "x4LZp_LCPS_ORG_AUT",
            "api_password": "n2L4Roj7J5Szt8Q3K",
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
            jsonUtils.write({"appearance_theme":self.__appearance.get()}, file=constants.PREFERENCES)
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
    
    def get_year_of_birth(self, font = ("None", 50)): # CustomQuestion
        def verify_and_continue():
            typed = typer.get().strip()
            year = datetime.now().year
            self.logger.info(f"User typed {typed} as input for date of birth")
            
            birth_year = re.sub(r"\D", "", typed)
            
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
        
        sheets = InformationPages()
        
        for d in apimedic_txt_config:
            d: dict
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
    '''Parent class to put UI diagnosis code for APImedic'''
    logger: Logger
    # for linting
    home: Callable
    quit: Callable
    clean: Callable
    mainloop: Callable
    raise_exception: Callable
    winfo_width: Callable
    winfo_height: Callable
    # improve API quiz by sorting through symptoms list
    # A) Ask how they're feeling on 1-10 scale. 7+ means we tell them to go to doctor right away (don't deal with that case)
    # B) Add data for each condition about part of body it's from (digestive, respiratory, etc.)
    # C) Ask user where pain is coming from (checkboxes)
    # D) Filter further by sublocations
    # E) Filter symptoms list by sublocations to make it shorter.
    def _diagnose(self) -> None:
        if not jsonUtils.read(constants.USER_DATA).get("disclaimer_read", False):
            self.disclaimer()
            self.clean()
        
        rating = self.scale_question()
        self.clean()
        self._stop_if_dangerous(rating)
        self.clean()
        
        filter_by_parts = self.body_parts()
        self.clean()
        # Get sublocations of filter_by_parts
        subparts = BodyParts()
        for part in jsonUtils.read(constants.BODY_LOCATIONS):
            if part["Name"].title() in filter_by_parts:
                subparts+=(x["Name"] for x in part["sublocations"])


        selected_subparts = self.body_parts(parts=subparts)

        self.logger.debug(f"IDS: {selected_subparts.subparts_to_ids()}")
        symptoms = Diagnosis(jsonUtils.get_values(), testing=constants.IS_TESTING).get_symptoms_by_sublocations(*selected_subparts.subparts_to_ids())

        self._get_filtered_medical_conditions(symptoms) # are you feeling any of the above from <list of possible symptoms>
        self.clean()
    
    def disclaimer(self) -> None:
        ctk.CTkLabel(self, text="DISCLAIMER", font=("", 50)).pack(pady=20)
        ctk.CTkLabel(
            self,
            text=disclaimer,
            wraplength=self.winfo_width()//2,
            font=("", 25),
            anchor=tk.W
        ).pack(pady=20)
        
        ctk.CTkButton(
            self,
            text="I accept",
            command=self.quit
        ).pack(pady=20)
        
        self.mainloop()
        jsonUtils.add({"disclaimer_read": True})
    
    def scale_question(self) -> int:
        ctk.CTkLabel(self, text="How much pain are you in on a scale of 1-10?", font=(None, 40)).pack(pady=20)
        scale = ctk.CTkSlider(
            self,
            from_=1,
            to=10,
            number_of_steps=9,
            width=self.winfo_width()//2,
            command=lambda v: l.configure(text=int(v))
        )
        scale.set(1)
        scale.pack(pady=80)
        
        l = ctk.CTkLabel(self, text=str(int(scale.get())), font=(None, 20))
        l.pack(pady=80)
        
        ctk.CTkButton(self, text="Continue", font=(None, 30), command=self.quit).pack(pady=40)
        
        self.mainloop()
        return int(scale.get())
    
    
    def _stop_if_dangerous(self, rating: int) -> None:
        '''Stops if user rated more than a 7'''
        if rating >= 7:
            ctk.CTkLabel(self, text="Please consult a Medical Professional", font=(None, 40)).pack(pady=self.winfo_height()//5)
            
            ctk.CTkButton(self, text="Quit", command=self.quit).pack(pady=50)
            self.mainloop()
            exit(0)
            
    
    def body_parts(self, parts: Iterable[str] | None = None) -> BodyParts:
        ctk.CTkLabel(self, text="Where are you feeling pain from?", font=(None, 40)).pack(pady=40)
        
        if parts is None:
            parts = [x["Name"] for x in jsonUtils.read(constants.BODY_LOCATIONS)]

        # set up checkboxes
        selected = {}
        for part in parts:
            selected[part] = tk.BooleanVar(value=False)
            ctk.CTkCheckBox(
                self,
                text=part,
                variable=selected[part],
                onvalue=True,
                offvalue=False
            ).pack(pady=20)
        
        ctk.CTkButton(self, text="Continue", command=self.quit).pack(pady=40)
        
        self.mainloop()
        return BodyParts(*(k for k, v in selected.items() if v.get()))
    
    def get_filtered_conditions(self, parts: BodyParts) -> tuple[dict]:
        ids = []
        for part in parts:
            # get ID of subpart
           pass 
        conditions = Diagnosis(jsonUtils.get_values(), testing=constants.IS_TESTING).get_symptoms_by_sublocation() 
        return conditions # type: ignore
        
    @staticmethod
    def filtermethod(condition_parts: list[str], parts: BodyParts) -> bool:
        return any(condition in parts for condition in condition_parts)

    def diagnosis_quiz(self) -> None:
        '''Gather diagnosis data and use it to call API'''
        def call_api(user):
            results = Diagnosis(
                user=user,
                testing=constants.IS_TESTING
            ).make_call()
            
            if isinstance(results, str) and results == "":
                self.raise_exception(
                    title="API Token Error",
                    message="An error occured while fetching diagnosis results.\nPlease check username and password",
                    icon="cancel"
                )
                self.logger.debug("Raised API Token Error")
                self.quit()
                self.home()
            
            self.logger.debug("User made daily diagnosis call.")
            
            f = constants.TODAY_DATE_FILE
            jsonUtils.overwrite(
                data = results, # type: ignore
                file = f
                )
            self.logger.info(f"Writing to log file {f} completed successfully")
        
        self.clean()
        
        x = MCQbuiler(
            self, # type: ignore
            "Daily Checkup",
            CustomQuestion(self._diagnose)
        ).begin(
            title_next="Data gathered!",
            continue_text="Diagnose me",
            next_button_width=300,
            next_button_height=70
        )
        
        self.quit()
        
        # user reported a 7+ pain level
        if x[0] == -1:
            self.clean()
            self.home()
            return
        
        # get keys user clicked on
        test_results: list[str] = [key for key, val in self._selected_conditions.items() if val.get()] # type: ignore
        user = jsonUtils.get_values()
        
        conditions = user.conditions.copy()
        
        for condition in test_results:
            # search for ID of condition
            self.logger.debug(f"Looking for ID of {condition}")
            conditions += [jsonUtils.search(
                constants.SYMPTOM_LOOKUP,
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
        
        
        diseases: list[dict] = jsonUtils.read(constants.TODAY_DATE_FILE) # type: ignore
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
                command=lambda name=name: webbrowser.open_new_tab(f"https://www.google.com/search?q={name.replace(' ', '%20')}") # type: ignore
            ).pack(pady=50)
        
        ctk.CTkButton(
            self,
            text="Back to homepage",
            command=self.quit
        ).pack()
        
        if loop:
            self.mainloop()
        
    def _get_filtered_medical_conditions(self, conditions: tuple[str]):
        self.clean()
        
        rows, columns = 15, 3
        
        total_names = len(conditions)

        # combine tuple of possible conditions into one
        conditions = itertools.chain(*conditions) # type: ignore

        for i in range(ceil(total_names/(rows*columns))):
            def continue_button():
                self.clean()
                self.quit()
                self.logger.debug(f"Onto page {i+1}")
            
            title = ctk.CTkLabel(
                self,
                text="Are you experiencing any of the above from this list?",
                font=(None, 50)
                )
            next_button = ctk.CTkButton(
                self,
                text="Continue",
                command=continue_button,
                width=280,
                height=56,
                font=(None, 40)
                )
            
            title.grid(
                column=0, 
                columnspan=10, 
                padx=5, 
                pady=20,
                sticky=tk.N
                )
            
            self._checkboxes(
                font=(None, 30), # type: ignore
                columns=columns,
                rows=rows,
                conditions=iter(conditions),
            )
            
            next_button.grid(row=rows+1, column=columns-1, sticky = tk.W, pady=30)
            next_button.lift()
            
            self.mainloop()
            print()

    def _checkboxes(
            self,
            conditions: Iterator,
            font: tuple[str, int] = ("Arial", 25),
            rows: int = 15,
            columns: int = 3
        ) -> None:
        '''Creates the checkboxes'''
        # make column outer loop so that things with long names get grouped into one column, saving space
        for j in range(columns):
            for i in range(1, rows+1):
                name = next(conditions, None)
                self.logger.debug(name)
                
                if name is None:
                    return
                name = name["Name"]
                
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
