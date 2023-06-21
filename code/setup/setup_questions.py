import tkinter as tk
import customtkinter as ctk
import re
from datetime import datetime
from CTkMessagebox import CTkMessagebox

from utils.parse_json import jsonUtils


preferences = "json/preferences.json"
user_data = "json/user-data.json"
conditions_list = "json/symptoms.json"


class Questions:
    '''Setup questions for application'''
    # TODO: Add information pages to tell user how to create API medic account
    def __init__(self) -> None:
        self.__appearance = tk.StringVar(value="light")
        self._selected_conditions: list = None
    
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
    
    def _get_previous_medical_conditions(self, font="Default") -> None: # CustomQuestion
        """Create checkboxes of previous medical conditions

        Parameters:
        -----------
            font (str, optional): font options for title and next button. Font size is immutable. Defaults to "Default".
        """
        
        def continue_button():
            self.__conditions = {key: value.get() for key, value in self.__conditions.items() if value.get()}
            self._selected_conditions = list(self.__conditions.keys())
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