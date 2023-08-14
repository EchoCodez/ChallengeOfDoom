from __future__ import annotations
from setup import *

class Program(Questions, ApiParent):
    """The main program that runs the application

    Parameters:
    -----------
        ctk (str): window background color, tuple: (light_color, dark_color) or single color
    """    
    
    def __init__(self) -> None:
        '''
        Initilize self and set up program, if not already set up
        '''
        
        super().__init__(logger=setup_logging())
        
        
        def quit_app(*events: object):
            self.logger.info("QUITTING")
            os._exit(0)
            
        self.title("Congressional App Challenge 2023")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<KeyPress-`>", quit_app) # for testing code faster
        self.bind("<Button-2>", quit_app) # for testing code faster

        self.geometry(f"1920x1080+0+0")
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
        
        if not jsonUtils.read(constants.PREFERENCES).get("setup_finished", False):
            self.setup()
            self.show_register_api_pages()
            jsonUtils.write({"setup_finished": True}, file=constants.PREFERENCES)
            self.logger.debug(jsonUtils.get_values())

        set_theme()
            
        
        medicines = jsonUtils.read(constants.MEDICINES)
        
        self.notifications = medicines
        self.logger.info("Loading medicine notifications into memory")
        for i in range(len(self.notifications)):
            notif = self.notifications.pop(0)
            self.add_notifs(notif)
            self.logger.debug(f"{self.notifications[i] = }")
        self.len = len(self.notifications)
        
        global print
        print = self.logger.debug
    
    def health_log(self) -> None:
        self.quit()
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
        self.quit()
        
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
        
        def _weather():
            self.clean()


            frame = ctk.CTkScrollableFrame(
                self,
                width=self.winfo_screenwidth()-100,
                height=self.winfo_screenheight()-100,
            )
            frame = self
            #_weather(frame, self.logger)


            weather_data = jsonUtils.read(constants.WEATHER_DATA)["main"]
            print(weather_data)
           


            # TODO: Take into account humidity and wind when giving recommendations
            ctk.CTkLabel(self, text="Weather").pack()


            def _weatherinfo():
                print("FFFFFFFFFFFFFFFFFFFFFFFF")
                def to_farenheit(cel: float) -> float:
                    return 32+9*cel/5
                
                location = jsonUtils.read(constants.USER_DATA).get("location", False)
                # TODO: use location to check if use_celsius should be true or false
                use_celsius = False
                weather =  f"{weather_data['temp']:.1f}\u2103" if use_celsius else f"{to_farenheit(weather_data['temp']):.0f}\u2109"
                ctk.CTkLabel(
                    self,
                    text=f"Current Weather: {weather}.\nHumidity: {weather_data['humidity']}%",
                    width=120,
                    height=32,
                    text_color="#FFFFFF",
                    font=("Times New Roman", 30)
                ).place(relx=0.7, rely=0.3, anchor=tk.CENTER)
            recommendation = ''

            if weather_data['temp'] <= -4:
                recommendation = "Wear a winter jacket. It is VERY cold outside."
            elif weather_data['temp'] > -4 and weather_data['temp'] <= 7:
                recommendation = 'Wear a light or medium coat. It is quite cold outside.'
            elif weather_data['temp'] > 7 and weather_data['temp'] <= 18:
                recommendation = 'Wear a fleece jacket. It is a bit chilly outside.'
            elif weather_data['temp'] > 18 and weather_data['temp'] <= 32:
                recommendation = 'Wear a short sleeved shirt. It is quite hot outside.'
            elif weather_data['temp'] > 32:
                recommendation = 'It is recommended that you don\'t go outside today. It is very hot outside.'

            def _recommendations():
                print('GGGGGGGGGGG')
                ctk.CTkLabel(
                    self,
                    text=recommendation,
                    width=120,
                    height=32,
                    text_color="#FFFFFF",
                    font=("Times New Roman", 30)
                ).place(relx=0.7, rely=0.7, anchor=tk.CENTER)


            
               
            ctk.CTkButton( # shows humidity and temp
                self,
                fg_color="#ADD8E6",
                command=_weatherinfo,
                text="Weather",
                width=300,
                height=350,
                border_width=1,
                corner_radius=40,
                text_color='#000000',
                font=("Times New Roman", 30)
                ).place(relx=0.2, rely=0.3, anchor=tk.CENTER)
            
            ctk.CTkButton( # shows recommendations
                self,
                fg_color="#ADD8E6",
                command=_recommendations,
                text="Recommendations",
                width=200,
                height=300,
                border_width=1,
                corner_radius=40,
                text_color='#000000',
                font=("Times New Roman", 30)
                ).place(relx=0.2, rely=0.7, anchor=tk.CENTER)

            ctk.CTkButton(
                self,
                text="Back to Homepage",
                command=self.home,
                fg_color="#3396FF",
                height=50,
                width=300,
                text_color='#FFFFFF',
                corner_radius=40
            ).place(relx=0.1, rely=0.95, anchor=tk.CENTER)
            self.mainloop()


        HomepageSection( # bottom
            self,
            text="Weather",
            command=_weather,
            fg_color="#ADD8E6",
            height=self.winfo_screenheight()*0.55,
            width=self.winfo_screenwidth()*0.2,
            text_color="#000000",
            font=("Times New Roman", 30),
            corner_radius=40,
            placement={"relx":0.5, "rely":0.5, "anchor":tk.CENTER}
            )
        
        def create_settings():
            self.clean()
            
            def leave():
                self.quit()
                self.home()

            ctk.CTkButton(
                self,
                text="Back to Homepage",
                command=leave
            ).pack(pady=20)
            Settings(
                self,
                self.logger,
                width=self.winfo_screenwidth()-100,
                height=self.winfo_screenheight()-140 # TODO: calculate this based on button size
            ).pack()
            # home already mainloops: don't do it manually
        
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
        
    def activate_notifs(self, notifications: list[Notification]) -> None:
        self.logger.debug("Scheduling notifications")
        for notif in notifications:
            # self.logger.debug("notif: {0}".format(notif))
            schedule.every().day.at(notif.time).do(notif.send)

    def add_minutes(self, data, hh, mm, i, minutes):
        return "{0} {1}".format(
            str(timedelta(
                seconds=int(hh) * 3600 + int(mm) * 60 + minutes
                ))[0:-3],
            data[self.labels[i+4]][-2] + data[self.labels[i+4]][-1]
            )

    def add_notifs(self, data):
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
        Debugging parameter to erase all data in constants.PREFERENCES.json and user-data.json
    '''

    if erase_data: # only for testing purposes; delete in final push
        jsonUtils.clearfiles()

    program = Program()
    
    program.execute()
    


if __name__ == "__main__":
    main(erase_data=False)
