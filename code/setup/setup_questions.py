import re
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from logging import Logger
from utils import jsonUtils


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
        self._conditions: GENERATOR = iter(d["Name"] for d in jsonUtils.open(conditions_list))
        self.total_condition_pages = None
    
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
        
        total_names = len(jsonUtils.open(conditions_list))
        
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
            text="Enter your location for specialists near you"
        ).pack(pady=100)
        
        texts: list[ctk.CTkEntry] = []
        for text in ("City", "State", "Country"):
            texts.append(ctk.CTkEntry(
                self,
                placeholder_text=text,
                width=280,
                height=56
            ))
            texts[-1].pack(pady=20)
        
        self.mainloop()
        return " ".join(t.get() for t in texts)
    