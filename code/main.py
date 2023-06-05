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
    
    def __init__(self, fg = None) -> None:
        '''
        Initilize self and set up program, if not already set up
        '''
        
        ctk.CTk.__init__(
            self=self,
            fg_color=fg
            )
        
        def quit_app(event):
            self.logger.info("QUITTING")
            sys.exit(0)
            
        self.logger = setup_logging()
        self.title("Congressional App Challenge 2023")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Button-2>", quit_app) # for testing code faster
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.focus_force()
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
        
        self.resizable(width=True, height=True)
        with open("json/medicines.json") as f:
            medicines = json.load(f)
        self.notifications: list[dict[str, str]] = medicines
        for i in range(len(self.notifications)):
            self.notifications[i] = Notification(
                "Medication Reminder",
                f"Take {self.notifications[i]['Morning']} dose of {self.notifications[i]['Medicine Name']}",
                self.notifications[i]["Breakfast Time"]
                )
            self.logger.debug(self.notifications[i])
        self.logger.debug("self.notifications: {0}".format(self.notifications))
        global print
        print = self.logger.debug
        
    
    def raise_exception(self, **kwargs) -> Exception:
        return CTkMessagebox(self, **kwargs)
    
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
        
        jsonUtils.write({
                "gender": answers[1],
            })
        
        self.clean()
        jsonUtils.write({"setup_finished": True}, file=preferences)
        self.logger.debug(jsonUtils.get_values())
    
    def _diagnose(self) -> None:
        def call_api(user):
            results = Diagnosis(user=user).make_call()
            
            self.logger.debug("User made daily diagnosis call.")
            file = f"json/health/{date.today().strftime('%d_%m_%y')}.json"
            jsonUtils.overwrite(
                data = results,
                file = file
                )
            self.logger.info(f"Writing to log file '{file}' completed successfully")
            
            # writes it to list of logs
            logs = set(jsonUtils.open("json/logs.json")["logs_list"]).union((file,))
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
    
    def open_health_log(self) -> None:
        MCQbuiler(
            self,
            "Daily Checkup",
            self.logger,
            CustomQuestion(self.get_previous_medical_conditions, kwargs={"file": "json/conditions.json"})
        ).begin()
     
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
        
        
        diseases = jsonUtils.read("json/possible_diseases.json")
        self.get_diagnosis_info(diseases, tabview, font)
        self.mainloop()
        
    def get_diagnosis_info(self, diseases: str|list[dict], tabview: ctk.CTkTabview, font = ("Times New Roman", 35), loop=False) -> None:
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
        
        ctk.CTkButton( # top left
            self,
            fg_color="#ADD8E6",
            text="Medicine Log",
            command=self.medicine,
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
            text="Settings",
            command=lambda: Settings(self, self.logger),
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

    def update(self) -> None:
        try:
            if self.notifications != tmp:
                notif = self.notifications[-1]
                schedule.every().day.at(notif.time).do(notif.send)
        except:
            pass
        schedule.run_pending()
        self.after(16, self.update)
        tmp = self.notifications
        

    def activate_notifs(self, notifications: list[Notification]) -> None:
        self.logger.debug(notifications)
        self.logger.debug("WHJKASN")
        for notif in notifications:
            self.logger.debug("notif: {0}".format(notif))
            self.logger.debug(notif.time)
            schedule.every().day.at(notif.time).do(notif.send)
            
        

    def execute(self) -> None:
        if not jsonUtils.open(preferences).get("setup_finished", False):
            self.setup()
        else:
            set_theme()
    
        try:
            os.system("taskkill /im thing.exe")
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
    