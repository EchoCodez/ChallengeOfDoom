from __future__ import annotations
from setup import *


preferences = "json/preferences.json"
user_data = "json/user-data.json"
conditions_list = "json/symptoms.json"

class Program(ctk.CTk, Questions):
    """The main program that runs the application

    Parameters:
    -----------
        ctk (str): window background color, tuple: (light_color, dark_color) or single color
    """    
    
    def __init__(self: Program, fg = None) -> None:
        '''
        Initilize self and set up program, if not already set up
        '''
        
        ctk.CTk.__init__(
            self=self,
            fg_color=fg
            )
        
        def quit_app(event):
            self.logger.info("QUITTING")
            os._exit(0)
            
        self.logger = setup_logging()
        self.title("Congressional App Challenge 2023")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Button-2>", quit_app) # for testing code faster
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.focus_force()
        self.labels = {
            0: "Medicine Name",
            1: "Morning", 
            2: "Afternoon", 
            3: "Evening",
            4: "Breakfast Time",
            5: "Lunch Time",
            6: "Dinner Time",
            7: "Before/After Meal",
        }
        if (self.winfo_screenwidth(), self.winfo_screenheight()) != (1920, 1080):
            self.logger.debug(f"Screen dimensions {self.winfo_screenwidth()}x{self.winfo_screenheight()} are not recommended")
            answer = self.raise_exception(
                title="Screen Dimensions",
                message=f"Your screen dimensions are not of the recommended 1980x1080 pixels. This may cause some errors.\
                    \nCurrent dimensions: {self.winfo_screenwidth()}x{self.winfo_screenheight()}",
                icon="warning",
                option_1="Quit",
                option_2="Understood",
            )
            if answer.get() == "Quit":
                self.on_closing()
        else:
            self.logger.debug("User has good screen dimensions")
        
        if not jsonUtils.open(preferences).get("setup_finished", False):
            Questions.__init__(
            self=self
            )
            self.setup()
            self.show_register_api_pages()
            jsonUtils.write({"setup_finished": True}, file=preferences)
            self.logger.debug(jsonUtils.get_values())

        set_theme()
            
        
        medicines = jsonUtils.read("json/medicines.json")
        
        self.notifications = medicines
        self.logger.info("Loading medicine notifications into memory")
        for i in range(len(self.notifications)):
            notif = self.notifications.pop(0)
            self.add_notifs(notif)
            self.logger.debug(self.notifications[i])
        self.len = len(self.notifications)
        
        global print
        print = self.logger.debug
        
    def raise_exception(self: Program, **kwargs) -> CTkMessagebox:
        return CTkMessagebox(self, **kwargs).mainloop()
    
    def on_closing(self) -> None:
        '''Confirm if user wanted to end application'''
        
        self.logger.info("User clicked X button")
        
        answer = self.raise_exception(
            title="Quit?",
            icon="question",
            message="Do you want to close the application?",
            option_1 = "Cancel",
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
            include_end=False
        )
        answers = prequiz.begin()
        
        jsonUtils.write({
                "gender": answers[1],
            })
        
        self.clean()
    
    def _diagnose(self) -> None:
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
            logs: list[str] = jsonUtils.open("json/logs.json")["logs_list"]
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
            CustomQuestion(self._get_previous_medical_conditions)
        ).begin(
            title_next="Data gathered!",
            continue_text="Diagnose me",
            next_button_width=300,
            next_button_height=70
            )
        
        self.quit()
        
        test_results = self._selected_conditions.copy()
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
     
    def _show_diagnosis_results(self: Program, font: str | tuple[str, int] = ("Times New Roman", 35)) -> None:
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
        
    def get_diagnosis_info(self: Program, diseases: str|list[dict], tabview: ctk.CTkTabview, font = ("Times New Roman", 35), loop=False) -> None:
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
    
    def health_log(self) -> None:    
        self.clean()
        self.logger.debug("Health Log Accessed")
        calendar = Calendar(self)
        calendar.run(mainloop=False)
            
        ctk.CTkButton(
            self,
            text="Back to Homepage",
            command=self.quit
        ).grid()
        
        self.mainloop()
        self.clean()
        self.home()
    
    def medicine(self) -> None:
        self.clean()
        self.logger.debug("Medicine Log Accessed")
        medicine = Medicine(self, self.logger)
        medicine.run()
        self.mainloop()
        self.clean()
        self.home()
    
    def home(self) -> None:
        '''Main function that executes the program'''
        self.logger.debug("Reached Home Screen")
        self.clean()
        
        HomepageSection( # top left
            self,
            fg_color="#ADD8E6",
            text="Health Log",
            command=self.health_log,
            corner_radius=40,
            height=self.winfo_screenheight()*0.55,
            width=self.winfo_screenwidth()*0.2,
            font=("Times New Roman", 30),
            text_color="#000000",
            placement={"relx":0.15, "rely":0.3, "anchor":tk.CENTER}
            )
        
        HomepageSection( # bottom right
            self,
            text="Daily Diagnosis",
            command=self._diagnose,
            fg_color="#ADD8E6",
            height=self.winfo_screenheight()*0.55,
            width=self.winfo_screenwidth()*0.2,
            text_color="#000000",
            font=("Times New Roman", 30),
            corner_radius=40,
            placement={"relx":0.85, "rely":0.6, "anchor":tk.CENTER}
            )
        
        def create_settings():
            frame = ctk.CTkScrollableFrame(
                self,
                width=self.winfo_screenwidth()-100,
                height=self.winfo_screenheight()-100
            ) # not working
            frame = self
            Settings(frame, self.logger)
        
        HomepageSection( # bottom left
            self,
            fg_color="#ADD8E6",
            text="Settings",
            command=create_settings,
            corner_radius=40,
            height=self.winfo_screenheight()*0.25,
            width=self.winfo_screenwidth()*0.2,
            font=("Times New Roman", 30),
            text_color="#000000",
            placement={"relx":0.15, "rely":0.75, "anchor":tk.CENTER}
            )
        
        HomepageSection( # top right
            self,
            text="Medicine Log",
            fg_color="#ADD8E6",
            command=self.medicine,
            corner_radius=40,
            height=self.winfo_screenheight()*0.25,
            width=self.winfo_screenwidth()*0.2,
            font=("Times New Roman", 30),
            text_color="#000000",
            placement={"relx":0.85, "rely":0.15, "anchor":tk.CENTER}
        )
        
        self.mainloop()

    def update(self) -> None:
        if len(self.notifications) != self.len:
            for i in range(self.len, len(self.notifications)):
                notif = self.notifications[i]
                schedule.every().day.at(notif.time).do(notif.send)
                print(notif)
            self.len = len(self.notifications)
        schedule.run_pending()
        self.after(16, self.update)
        
    def activate_notifs(self: Program, notifications: list[Notification]) -> None:
        self.logger.debug("Scheduling notifications")
        for notif in notifications:
            # self.logger.debug("notif: {0}".format(notif))
            schedule.every().day.at(notif.time).do(notif.send)

    def add_minutes(self: Program, data, hh, mm, i, minutes):
        return "{0} {1}".format(
            str(timedelta(
                seconds=int(hh) * 3600 + int(mm) * 60 + minutes
                ))[0:-3],
            data[self.labels[i+4]][-2] + data[self.labels[i+4]][-1]
            )

    def add_notifs(self: Program, data):
        for i in range(3):
            hh, mm = data[self.labels[i+4]][0:-2].split(":")
            before = False
            if data[self.labels[7]] == "Before":
                before = True
            else:
                before = False
            for j in range(3):
                minutes = 0
                if j == 0:
                    minutes -= 1800
                if j == 2:
                    minutes += 1800
                if before:
                    minutes -= 1800
                if data[self.labels[i+1]] != "0":
                    self.notifications.append(Notification(
                        "Medication Reminder",
                        f"Take {data[self.labels[i+1]]} dose of {data['Medicine Name']} {data[self.labels[7]].lower()} {self.labels[i+4].lower()}",
                        self.add_minutes(data, hh, mm, i, minutes),
                        self.logger
                        ))

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

    def execute(self) -> None:    
        try:
            os.system("taskkill /im HealthApp.exe")
        except Exception: # ignore keyboard interrupt
            pass
        
        self.activate_notifs(self.notifications)
        self.after(0, self.update())
        self.home()


def main(*, erase_data: bool = False) -> None:
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
