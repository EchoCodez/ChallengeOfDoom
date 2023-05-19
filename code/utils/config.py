from utils import jsonUtils
import customtkinter as ctk
import tkinter as tk
import logging


def set_theme() -> bool:
    '''Check if theme preference in file already.
    
    Returns:
    --------
        bool: whether or not appearance theme was found
    '''
    
    with open("json/preferences.json") as f:
        if jsonUtils.get(f, "appearance_theme", func = ctk.set_appearance_mode):
            return True
    return False

def delete_old_diagnosis(logger):
    from datetime import date
    
    logger.info("Attempting to save memory by deleting last months checkup results")
        
    current_date = date.today()
    current_month = current_date.month
    last_month = current_month - 1 if current_month != 1 else 12  
    today_a_month_ago = date(current_date.year, last_month, current_date.day).strftime("%d_%m_%y")
    
    last_months_checkup = f"json/logs/{today_a_month_ago}.json"
    try:
        jsonUtils.delete_file(last_months_checkup)
    except FileNotFoundError:
        logger.info(f"Last months checkup was not found. AKA file path {last_months_checkup} was not found.")
        return
    else:
        logger.info("Deletion of last months diagnosis was successfull")
    
    logger.info("Attempting to remove it from json/logs.json")
    
    try:
        data = jsonUtils.open("json/logs.json")["logs_list"]
        jsonUtils.overwrite(
            data = {"logs_list": [x for x in data if x != last_months_checkup]},
            file="json/logs.json"
            )
    except Exception as e:
        logger.warning(e)
    else:
        logger.info(f"Removed {last_months_checkup} from json/logs.json")

class Settings:
    def __init__(self, master: ctk.CTk, logger: logging.Logger) -> None:
        self.master = master
        self.logger = logger
        self.logger.debug("Settings Clicked")
        self.show_settings()
    
    def show_settings(self, mainloop=True, font=""):
        self.master.clean()
        self.setting_vars = []
        
        def swap_mode():
            ctk.set_appearance_mode("dark" if ctk.get_appearance_mode().lower()=="light" else "light")
            self.logger.debug(f"Swapped appearance mode to {ctk.get_appearance_mode()}")
            # TODO: Write to file
            
        
        
        self.setting_vars += self.create_switch_setting("Toggle Appearance Mode", command=swap_mode),
        
        if mainloop:
            self.master.mainloop()
    
    def create_switch_setting(self, name: str, **kwargs) -> tk.Variable:
        """Create a setting button controlled by a switch

        Parameters:
        -----------
            name (str): Setting name
            
            ACCEPTABLE KWARGS: width, height, font, switch_font, var, switch_place_kwargs, label_place_kwargs, on_off,
            command, switch_kwargs, label_kwargs

        Raises:
        -------
            TypeError: Unknown kwarg passed in

        Returns:
        --------
            tk.Variable: The variable after being attached to the button
        """
        
        width, height = kwargs.pop("width", 300), kwargs.pop("height", 72)
        font, switch_font = kwargs.pop("font", ("", 50)), kwargs.pop("switch_font", None)
        var = kwargs.pop("var", tk.StringVar())
        switch_kwargs = kwargs.pop("switch_place_kwargs", {"relx":0.7, "rely":0.1, "anchor":tk.CENTER})
        label_kwargs = kwargs.pop("label_place_kwargs", {"relx":0.2, "rely":0.1, "anchor":tk.CENTER})
        on, off = kwargs.pop("on_off", ("on", "off"))
        command = kwargs.pop("command")
        switch_creation_kwargs, label_creation_kwargs = kwargs.pop("switch_kwargs", {}), kwargs.pop("label_kwargs", {})
        
        if kwargs:
            raise TypeError("Invalid kwargs {0}".format(kwargs))
        
        l = ctk.CTkLabel(
            self.master,
            text=name,
            font=font,
            **label_creation_kwargs
        )
        ctk.CTkSwitch(
            self.master,
            onvalue=on,
            offvalue=off,
            variable=var,
            command=command,
            switch_width=width,
            switch_height=height,
            font=switch_font,
            text="",
            **switch_creation_kwargs
        ).place(**switch_kwargs)
        l.place(**label_kwargs)
        return var

if __name__ == "__main__":
    r = ctk.CTk()
    r.geometry("720x480")
    Settings(r)
